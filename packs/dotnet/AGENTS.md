## .NET Conventions

**Toolchain:** dotnet CLI (build, test, publish), NUnit (testing), coverlet (coverage), editorconfig (style enforcement).

**Setup verification:** Before writing code, confirm: `dotnet --version` (>= 10.0). If a `Directory.Packages.props` exists, all package versions are managed centrally — never add `Version=` attributes to individual `PackageReference` entries.

**Package management:** Use central package management via `Directory.Packages.props`. Add new packages with `dotnet add package <name>` then move the version to `Directory.Packages.props`. Use the private feed in `nuget.config` for internal packages — do not add alternative feeds without review.

**Code style:** File-scoped namespaces (`namespace X;` not `namespace X { }`). Nullable reference types enabled. Follow `.editorconfig` rules. No `#pragma warning disable` unless the reason is documented inline.

**Project structure:** Clean Architecture — `src/` contains Core (domain), Application (use cases), Infrastructure (external concerns), FunctionApp/API (entry point). `tst/` mirrors `src/` with UnitTests, IntegrationTests, and ComponentTests per layer.

**Testing:** Tests live in `tst/`. Run with `dotnet test`. Use `coverlet.runsettings` for coverage configuration. Every error path needs a test. Use Moq for mocking. Name tests: `MethodName_Scenario_ExpectedResult`.

**Acceptance criteria:**
- [ ] `dotnet build` succeeds with zero warnings
- [ ] `dotnet test` passes all unit and component tests
- [ ] No `Version=` in individual `.csproj` files (central management only)
- [ ] No unhandled error paths in new code
- [ ] New public APIs have XML doc comments
