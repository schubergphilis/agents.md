# Reusable Prompts Library

## Purpose

This directory contains **project-agnostic, reusable prompts** that can be used across any software development project. These prompts are:

- **Technology-neutral**: No references to specific frameworks, languages, or tools
- **Domain-independent**: No references to specific business domains or use cases  
- **Configuration-free**: Self-contained with sensible defaults
- **Composable**: Designed to work together through tag-based references

## File Structure

Each prompt follows the naming convention: `{primary_tag}.md`

For example:
- `feature_dev.md` - Main feature development prompt (`#feature_dev`)
- `debug_bug.md` - Bug debugging methodology (`#debug_bug`) 
- `run_all_tests.md` - Test execution building block (`#run_all_tests`)

## Configuration

Optional project-specific customisations are handled through corresponding files in `prompts/config/`, e.g.:
- `prompts/config/feature_dev.md` - Project-specific feature development preferences
- `prompts/config/debug_bug.md` - Project-specific debugging workflows
- `prompts/config/tech_stack.md` - Technology stack specific patterns

## Usage

Reference prompts using hashtags:
```
Use #feature_dev to implement the new user authentication system
```

Combine multiple prompts:
```  
Use #context_intake then #test_plan then #feature_dev for the dashboard feature
```

## Contributing

When adding new prompts:

1. **Keep it generic** - No project-specific references
2. **Make it composable** - Reference other prompts via tags
3. **Include examples** - Show common usage patterns
4. **Cross-reference** - Add "Related Prompts" sections
5. **Test reusability** - Ensure prompt works across different contexts

See `./prompts/contributing.md` for detailed guidelines.
