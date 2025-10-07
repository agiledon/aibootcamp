# CrewAI DDD Expert

A CrewAI-powered system that implements Domain-Driven Design (DDD) methodologies and processes to perform domain modeling from requirements, generating both domain layer product code and test code.

## Overview

This project leverages CrewAI to create an intelligent crew of AI agents that work collaboratively to transform business requirements into well-structured domain models following DDD principles. The system consists of three specialized agents working in sequence to deliver complete domain modeling solutions.

## Features

- **Domain Modeling**: Automatically analyzes business requirements and creates domain models using DDD principles
- **Code Generation**: Generates Java code implementing the domain model with proper DDD patterns
- **Unit Testing**: Creates comprehensive unit tests for the generated domain layer code
- **PlantUML Integration**: Generates UML class diagrams using PlantUML syntax
- **Multi-Agent Collaboration**: Uses specialized agents for different aspects of the development process

## Architecture

The system consists of three specialized AI agents:

### 1. Domain Expert Agent
- **Role**: DDD domain modeling expert
- **Responsibility**: Analyzes business requirements and creates domain models following DDD principles
- **Output**: Markdown domain model documentation with PlantUML diagrams
- **LLM**: `ollama/deepseek-r1:7b`

### 2. Developer Agent
- **Role**: Java development engineer specialized in DDD
- **Responsibility**: Converts domain model documentation into Java code implementation
- **Output**: Java classes following DDD patterns (AggregateRoot, Entity, ValueObject)
- **LLM**: `ollama/qwen2.5-coder:7b`

### 3. Tester Agent
- **Role**: Unit testing specialist
- **Responsibility**: Creates comprehensive unit tests for the generated domain code
- **Output**: JUnit5 test classes with Mockito and AssertJ
- **LLM**: `ollama/qwen2.5-coder:7b`

## Installation

### Prerequisites

- Python >= 3.12
- UV package manager (recommended)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd agent/crewai_ddd_expert
```

2. Install dependencies:
```bash
uv sync
```

3. Ensure Ollama is running with the required models:
```bash
# Install required models
ollama pull deepseek-r1:7b
ollama pull qwen2.5-coder:7b
```

## Usage

### Running the Crew

Execute the main crew workflow:

```bash
uv run run_crew
```

Or run directly:

```bash
uv run src/crewai_ddd_expert/main.py
```

### Configuration

The system uses YAML configuration files for agents and tasks:

- `src/crewai_ddd_expert/config/agents.yaml`: Agent configurations
- `src/crewai_ddd_expert/config/tasks.yaml`: Task definitions

### Example Output

The system generates the following outputs in the `output/` directory:

1. **`domain_model.md`**: Domain model documentation with PlantUML diagrams
2. **`domain_model.java`**: Java implementation of the domain model
3. **`domain_model_test.java`**: Unit tests for the domain classes

## Example Domain Model

The system can handle complex business domains. For example, it can model an online meeting lifecycle management system with:

- **Meeting Lifecycle**: Pre-meeting, during-meeting, and post-meeting phases
- **Calendar Integration**: Google Calendar and Outlook integration
- **Workspace Management**: User workspaces with member management and permissions
- **Real-time Translation**: Meeting assistant bots for multilingual support
- **Resource Management**: Meeting recordings, transcripts, and documents

## DDD Patterns Implemented

The generated code follows key DDD patterns:

- **AggregateRoot**: Root entities that maintain consistency boundaries
- **Entity**: Objects with distinct identity
- **ValueObject**: Immutable objects defined by their attributes
- **Repository Pattern**: Data access abstraction
- **Domain Services**: Business logic that doesn't belong to entities

## Code Quality Standards

The generated code follows these standards:

- **Naming Conventions**: CamelCase for classes, snake_case for test methods
- **Package Structure**: Organized by domain concepts
- **Documentation**: Markdown-formatted class comments
- **Testing**: Given-When-Then pattern for test methods
- **Mocking**: Mockito for external dependencies
- **Assertions**: AssertJ for fluent assertions

## Workflow Process

1. **Requirement Analysis**: The domain expert analyzes business requirements
2. **Domain Modeling**: Creates domain model with PlantUML diagrams
3. **Code Generation**: Developer converts model to Java implementation
4. **Test Creation**: Tester generates comprehensive unit tests
5. **Output Generation**: All artifacts saved to output directory

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Contributors

### Zhang Yi
AI Strategy Consultant and AI-Native Application Developer, DDD Evangelist, Enterprise Mentor at Nanjing University DevOps+ Research Lab.

- GitHub: [@agiledon](https://github.com/agiledon)

## Support

For issues and questions, please open an issue in the repository or contact the development team.

## Future Enhancements

- Support for additional programming languages
- Integration with more LLM providers
- Enhanced PlantUML diagram generation
- Real-time collaboration features
- API endpoints for remote execution