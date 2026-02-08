# Context Server Integration

This reference explains how to use MCP (Model Context Protocol) servers to dynamically fetch up-to-date information instead of relying on static documentation.

## Why Use Context Servers

Context servers provide several advantages over static documentation:

- **Up-to-date Information**: Get the latest FastAPI, SQLModel, and SQLAlchemy documentation
- **Reduced Context Consumption**: Avoid embedding large amounts of static content
- **Dynamic Updates**: Information is fetched in real-time as needed
- **Accurate Details**: Always get current API references and best practices

## Using Context7 MCP Server

The `context7` MCP server provides access to:

### FastAPI Documentation
- Latest API references
- Updated features and deprecations
- Current best practices
- Example code snippets

### SQLModel/SQLAlchemy Resources
- Current ORM patterns
- Updated syntax and features
- Performance optimization techniques
- Migration guides

### Security Best Practices
- Current security recommendations
- Updated authentication patterns
- Latest vulnerability information
- Secure coding practices

## Integration Patterns

### 1. Documentation Lookup
Instead of embedding documentation, use the context server to fetch current information:

```
Use context7 server to lookup:
- FastAPI dependency injection patterns
- SQLModel async session management
- Current security middleware implementations
- Latest testing patterns
```

### 2. Code Generation Assistance
Use the context server to get current syntax and patterns:

```
Fetch from context7:
- Current FastAPI decorator syntax
- Updated Pydantic v2 patterns
- SQLModel relationship definitions
- Modern async/await patterns
```

### 3. Troubleshooting Support
Use the context server for troubleshooting:

```
Query context7 for:
- Error resolution patterns
- Performance optimization techniques
- Common integration issues
- Compatibility considerations
```

## Best Practices

### When to Use Context Servers
- For detailed API documentation
- For current syntax and patterns
- For troubleshooting complex issues
- For security best practices
- For performance optimization

### When to Use Static References
- For high-level architectural patterns
- For project structure guidelines
- For common workflow patterns
- For configuration templates

### Combining Both Approaches
- Use static references for stable, well-established patterns
- Use context servers for dynamic, frequently updated information
- Reference both in skill instructions where appropriate
- Provide fallback information when context servers are unavailable

## Example Workflow

1. Start with static references for overall structure
2. Use context7 server to fill in current implementation details
3. Verify patterns against latest documentation
4. Apply best practices from current security guidelines