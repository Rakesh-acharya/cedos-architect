"""
Integration Tests - Test complete workflows
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from app.core.config import settings
from app.models.user import User, UserRole
from app.models.project import Project, ProjectType
from app.models.calculation import Calculation, CalculationType
from app.core.security import get_password_hash

# Test database
TEST_DATABASE_URL = "sqlite:///./test_cedos.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    """Create test database"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user(db):
    """Create test user"""
    user = User(
        email="test@cedos.com",
        username="testuser",
        full_name="Test User",
        role=UserRole.ENGINEER,
        hashed_password=get_password_hash("test123"),
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def test_project(db, test_user):
    """Create test project"""
    project = Project(
        project_code="TEST-001",
        project_name="Test Project",
        project_type=ProjectType.RESIDENTIAL_BUILDING,
        location="Test Location",
        usage_type="residential",
        seismic_zone="Zone III",
        soil_bearing_capacity=200,
        created_by=test_user.id
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

class TestCompleteWorkflow:
    """Test complete project workflows"""
    
    def test_project_creation_to_boq(self, db, test_user, test_project):
        """Test complete workflow: Project → Calculation → BOQ"""
        from app.models.calculation import Calculation, CalculationType, CalculationStatus
        from app.models.material import BOQ, BOQItem
        from app.services.engineering_calculations import StructuralDesignEngine
        from app.services.boq_calculator import BOQCalculator
        
        # Create calculation
        engine = StructuralDesignEngine()
        design = engine.design_column(
            axial_load=2000,
            concrete_grade="M25",
            steel_grade="Fe415"
        )
        
        calculation = Calculation(
            project_id=test_project.id,
            calculation_code="CALC-TEST-001",
            calculation_type=CalculationType.COLUMN_DESIGN,
            input_parameters={"axial_load": 2000},
            calculation_results={"design_completed": True},
            design_outputs=design,
            status=CalculationStatus.COMPLETED,
            code_standard_used="IS 456:2000",
            created_by=test_user.id
        )
        
        db.add(calculation)
        db.commit()
        db.refresh(calculation)
        
        # Generate BOQ
        boq_calc = BOQCalculator(db)
        calculations = [calculation]
        quantities = boq_calc.calculate_material_quantities(calculations)
        
        assert quantities["concrete"] > 0
        assert quantities["steel"] > 0
        
        # Create BOQ
        boq = BOQ(
            project_id=test_project.id,
            boq_code="BOQ-TEST-001",
            boq_name="Test BOQ",
            total_concrete_quantity=quantities["concrete"],
            total_steel_quantity=quantities["steel"]
        )
        
        db.add(boq)
        db.commit()
        
        assert boq.id is not None
        assert boq.total_steel_quantity > 0
    
    def test_cost_estimation_workflow(self, db, test_project, test_user):
        """Test cost estimation workflow"""
        from app.models.material import BOQ, BOQItem
        from app.models.cost import CostEstimate, CostItem
        
        # Create BOQ
        boq = BOQ(
            project_id=test_project.id,
            boq_code="BOQ-COST-001",
            boq_name="Test BOQ",
            total_concrete_quantity=10.0,
            total_steel_quantity=1000.0
        )
        db.add(boq)
        db.commit()
        db.refresh(boq)
        
        # Add items
        item1 = BOQItem(
            boq_id=boq.id,
            item_code="CONC-001",
            item_description="Concrete M25",
            item_category="Concrete",
            quantity=10.0,
            unit="m³",
            unit_rate=5000.0,
            total_amount=50000.0
        )
        
        db.add(item1)
        db.commit()
        
        # Create cost estimate
        estimate = CostEstimate(
            project_id=test_project.id,
            estimate_code="EST-001",
            estimate_name="Test Estimate",
            estimate_type="detailed",
            base_cost=50000.0,
            contingency_percentage=0.10,
            contingency_amount=5000.0,
            gst_percentage=0.18,
            gst_amount=9900.0,
            total_cost=64900.0
        )
        
        db.add(estimate)
        db.commit()
        db.refresh(estimate)
        
        assert estimate.total_cost == 64900.0
        assert estimate.base_cost == 50000.0

class TestDataIntegrity:
    """Test data integrity"""
    
    def test_calculation_results_consistency(self, db, test_project, test_user):
        """Test calculation results are consistent"""
        from app.services.engineering_calculations import StructuralDesignEngine
        from app.models.calculation import Calculation, CalculationType, CalculationStatus
        
        engine = StructuralDesignEngine()
        
        # Design same column twice
        design1 = engine.design_column(
            axial_load=2000,
            concrete_grade="M25",
            steel_grade="Fe415"
        )
        
        design2 = engine.design_column(
            axial_load=2000,
            concrete_grade="M25",
            steel_grade="Fe415"
        )
        
        # Results should be identical (deterministic)
        assert design1["column_size"] == design2["column_size"]
        assert design1["steel_area_required"] == design2["steel_area_required"]
    
    def test_boq_quantities_accuracy(self, db, test_project):
        """Test BOQ quantities are accurate"""
        from app.services.boq_calculator import BOQCalculator
        from app.models.calculation import Calculation, CalculationType, CalculationStatus
        
        # Create calculation
        calc = Calculation(
            project_id=test_project.id,
            calculation_code="TEST-BOQ",
            calculation_type=CalculationType.COLUMN_DESIGN,
            input_parameters={"axial_load": 2000},
            calculation_results={},
            design_outputs={
                "column_size": 0.5,
                "steel_area_required": 2500  # mm²
            },
            status=CalculationStatus.COMPLETED,
            created_by=test_user.id
        )
        db.add(calc)
        db.commit()
        
        # Calculate BOQ
        boq_calc = BOQCalculator(db)
        quantities = boq_calc.calculate_material_quantities([calc])
        
        # Verify quantities are positive
        assert quantities["concrete"] > 0
        assert quantities["steel"] > 0
        assert quantities["cement"] > 0
