# CEDOS Architecture Documentation

## System Overview

CEDOS (Civil Engineering Digital Operating System) is a comprehensive rule-driven engineering platform that automates civil engineering workflows from design to audit.

## Architecture Principles

1. **Rule-Driven**: All calculations follow codified engineering standards (IS codes, IRC, NBC)
2. **AI-Assisted**: AI provides explanations and suggestions but never bypasses rules
3. **Audit-Ready**: Every action is logged for legal traceability
4. **Modular**: System is built in independent, testable modules
5. **Secure**: Role-based access control and tamper-proof audit trails

## System Architecture

### Backend Architecture

```
backend/
├── app/
│   ├── api/              # API endpoints (REST)
│   │   └── v1/
│   │       └── endpoints/
│   ├── core/             # Core configuration
│   │   ├── config.py     # Settings
│   │   ├── database.py   # DB connection
│   │   └── security.py   # Auth & encryption
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   └── services/         # Business logic
│       ├── engineering_calculations.py
│       ├── boq_calculator.py
│       ├── compliance_checker.py
│       ├── cost_estimator.py
│       ├── document_generator.py
│       ├── ai_assistant.py
│       └── audit_logger.py
└── alembic/              # Database migrations
```

### Frontend Architecture

```
frontend/
├── src/
│   ├── components/       # Reusable components
│   ├── pages/           # Page components
│   ├── services/        # API clients
│   └── utils/           # Utilities
```

## Data Flow

### 1. Project Creation Flow

```
User Input → API Endpoint → Validation → Database → Audit Log
```

### 2. Calculation Flow

```
Input Parameters → Engineering Engine → Design Outputs → Compliance Check → Results
```

### 3. BOQ Generation Flow

```
Calculations → Material Quantities → BOQ Items → Cost Estimation
```

## Key Modules

### 1. Engineering Calculation Engine

**Purpose**: Performs structural design calculations following IS codes

**Key Functions**:
- Load calculations (Dead, Live, Wind, Seismic)
- Structural member design (Footings, Columns, Beams, Slabs)
- Safety factor checks

**Rules Applied**:
- IS 456:2000 (Concrete structures)
- IS 875 (Loads)
- IS 1893 (Seismic)

### 2. Compliance Checker

**Purpose**: Validates designs against code requirements

**Checks Performed**:
- Safety factors
- Minimum dimensions
- Reinforcement limits
- Code compliance

**Output**: Compliance status (Compliant/Non-Compliant/Warning)

### 3. Material Recommendation Engine

**Purpose**: Recommends material grades based on requirements

**Factors Considered**:
- Load intensity
- Exposure conditions
- Durability requirements
- Cost optimization

### 4. BOQ Calculator

**Purpose**: Automatically generates Bill of Quantities

**Process**:
1. Extract quantities from calculations
2. Apply wastage factors
3. Generate itemized BOQ
4. Map to material grades

### 5. Cost Estimator

**Purpose**: Generates cost estimates

**Features**:
- SOR integration
- Market rate support
- Escalation calculation
- GST calculation
- Contingency handling

### 6. Audit Logger

**Purpose**: Maintains tamper-proof audit trail

**Logged Actions**:
- All calculations
- All approvals
- All overrides
- All changes

## Security Model

### Authentication
- JWT-based authentication
- Token expiration
- Password hashing (bcrypt)

### Authorization
- Role-based access control
- 7 user roles (Engineer, Senior Engineer, PM, QS, Auditor, Gov Officer, Admin)
- Permission-based endpoints

### Audit Trail
- Every action logged
- User tracking
- IP address logging
- Timestamp tracking
- Tamper-proof (immutable logs)

## Database Schema

### Core Entities

1. **Users**: User accounts and roles
2. **Projects**: Project information
3. **Calculations**: Design calculations
4. **BOQ**: Bill of Quantities
5. **Cost Estimates**: Cost estimates
6. **Compliance Checks**: Code compliance records
7. **Documents**: Generated documents
8. **Audit Logs**: Audit trail

## API Design

### RESTful Endpoints

- `/api/v1/auth/*` - Authentication
- `/api/v1/projects/*` - Project management
- `/api/v1/calculations/*` - Calculations
- `/api/v1/boq/*` - BOQ management
- `/api/v1/cost/*` - Cost estimation
- `/api/v1/compliance/*` - Compliance checks
- `/api/v1/documents/*` - Document generation
- `/api/v1/execution/*` - Execution tracking

### Response Format

```json
{
  "data": {...},
  "status": "success",
  "message": "..."
}
```

## Engineering Rules

### Load Combinations (IS 456)

1. DL + LL
2. DL + LL + WL
3. DL + LL + SL
4. DL + WL
5. DL + SL
6. 0.9DL + WL
7. 0.9DL + SL

### Safety Factors

- Concrete: 1.5
- Steel: 1.15
- Overturning: 1.5
- Sliding: 1.5

### Material Grades

**Concrete**: M20, M25, M30, M35, M40
**Steel**: Fe415, Fe500, Fe550
**Cement**: OPC 43, OPC 53, PPC

## AI Integration

### Controlled AI Usage

AI is used ONLY for:
- Explaining design logic
- Suggesting optimizations
- Answering queries
- Error detection

AI NEVER:
- Bypasses code rules
- Makes design decisions
- Overrides safety factors
- Skips compliance checks

## Testing Strategy

### Unit Tests
- Engineering calculations
- Material recommendations
- Compliance checks

### Integration Tests
- API endpoints
- Database operations
- Service integrations

### Validation Tests
- Boundary conditions
- Edge cases
- Error handling

## Deployment Considerations

### Backend
- FastAPI with Uvicorn
- PostgreSQL database
- Redis (optional, for caching)
- Nginx (reverse proxy)

### Frontend
- React with Vite
- Nginx (static hosting)
- CDN (optional)

### Monitoring
- Application logs
- Error tracking
- Performance monitoring
- Audit log monitoring

## Scalability

### Horizontal Scaling
- Stateless API design
- Database connection pooling
- Load balancing

### Vertical Scaling
- Database optimization
- Query optimization
- Caching strategies

## Future Enhancements

1. BIM integration
2. CAD export
3. Advanced AI features
4. Mobile app
5. Real-time collaboration
6. Advanced reporting
7. Integration with external systems
