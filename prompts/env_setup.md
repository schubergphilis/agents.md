# Environment Setup and Reproduction

**Tags**: #env_setup #infrastructure  
**Purpose**: Set up development, testing, or production environments reliably and reproducibly  
**Configurable**: Yes - Technology stack, infrastructure tools, and deployment patterns

## Quick Usage

```
Use #env_setup to establish [development/testing/staging] environment for [project/service]
```

## Full Prompt

Set up reliable, reproducible environments for development and deployment:

**1. Environment Requirements Analysis**
- Apply #context_intake to understand project dependencies and requirements
- Identify required services, databases, and external integrations
- Document version requirements for languages, frameworks, and tools
- Note environment-specific configuration needs

**2. Development Environment Setup**
- Install and configure required development tools and dependencies
- Apply #env_repro to ensure consistent setup across different machines
- Set up local databases, seed data, and test fixtures
- Configure development servers, hot reloading, and debugging tools

**3. Service Dependencies Configuration**
- Set up required external services (databases, caches, message queues)
- Configure service discovery and inter-service communication
- Implement health checks and service monitoring
- Document service startup order and dependencies

**4. Configuration Management**
- Implement environment-specific configuration patterns
- Set up secure secret management for API keys and credentials
- Configure logging, monitoring, and debugging tools
- Establish environment variable patterns and validation

**5. Documentation and Automation**
- Apply #doc_update to create setup documentation and troubleshooting guides
- Create automated setup scripts and environment validation checks
- Document common issues and their resolutions
- Establish environment refresh and update procedures

Technology-specific setup patterns: See prompts_config/tech_stack.md  
Infrastructure and deployment approaches: See prompts_config/infrastructure.md

## Configuration Points

- **Technology Stack**: Language runtimes, framework setup, and build tools
- **Infrastructure**: Containerization, orchestration, and service management
- **Development Tools**: IDEs, debuggers, testing frameworks, and productivity tools
- **Security**: Secret management, access controls, and security scanning
- **Monitoring**: Logging, metrics collection, and debugging capabilities

## Related Prompts

**Prerequisites**: #context_intake - Understand project requirements and dependencies  
**Complements**: #env_repro, #infra_change - Environment consistency and modifications  
**Follows**: #feature_dev, #debug_bug - Use established environment for development

## Examples

**New Developer Onboarding**: "Set up local development environment for web application"
- Install Node.js, database, and required development tools
- Clone repositories and configure local services
- Set up IDE, debugging tools, and testing environment
- Validate setup with test suite and sample workflows

**Staging Environment**: "Reproduce production issues in controlled environment"
- Mirror production configuration and data patterns
- Set up monitoring and logging identical to production
- Configure load testing and performance measurement tools
- Establish deployment and rollback procedures

**CI/CD Pipeline**: "Set up automated testing and deployment environment"
- Configure build servers and automated testing infrastructure
- Set up artifact storage and deployment automation
- Implement security scanning and quality gate automation
- Establish monitoring and alerting for build pipeline health
