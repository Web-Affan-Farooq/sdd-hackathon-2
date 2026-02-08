# Refactored FastAPI Backend Development Skill

This document explains the refactored structure of the `backend-fastapi` skill and how it addresses the context window consumption issue.

## Problem Addressed

The original skill consumed excessive context by embedding:
- Complete project folder structures
- Full requirements.txt content
- Extensive code examples
- Detailed deployment configurations
- Comprehensive implementation patterns

## Solution Implemented

The skill has been refactored to:

1. **Move detailed content to reference files** in the `references/` directory
2. **Keep the main SKILL.md focused on essential guidance**
3. **Reference external files instead of embedding content**
4. **Integrate with MCP servers for dynamic information**

## New Structure

```
.backend-fastapi/
├── SKILL.md                    # Main skill file (minimal content)
└── references/                 # Detailed reference files
    ├── folder-structure.md     # Project structure details
    ├── dependency-management.md # UV package management
    ├── best-practices.md       # Implementation best practices
    ├── crud-operations.md      # Async CRUD patterns
    ├── database-session.md     # Database session management
    ├── deployment.md          # Deployment strategies
    ├── testing-patterns.md    # Testing strategies (existing)
    ├── refactoring-patterns.md # Refactoring guidelines (existing)
    ├── context-server-integration.md # MCP server usage
    └── ...                    # Other reference files
```

## Benefits

- **Reduced Context Consumption**: Main skill file is now ~20KB vs. previous ~50KB+
- **Maintainable**: Easy to update individual reference files
- **Extensible**: New topics can be added as separate reference files
- **MCP Integration**: Leverages dynamic information from context servers
- **Modular**: Each topic is contained in its own focused document

## Usage Instructions

1. **For general guidance**: Refer to the main `SKILL.md` file
2. **For detailed implementation**: Check the relevant reference files
3. **For current documentation**: Use the `context7` MCP server as directed
4. **For specific patterns**: Look up the appropriate reference file

## MCP Server Integration

The skill now encourages using the `context7` MCP server for:
- Latest FastAPI API documentation
- Current SQLModel/SQLAlchemy patterns
- Updated security best practices
- Performance optimization techniques
- Troubleshooting assistance

This reduces the need to embed potentially outdated information while ensuring access to current best practices.

