# Execute SonarQube Analysis — Maven (Java)

## Prerequisites

- The target project must be a Maven project (a `pom.xml` must exist at the project root or module root).
- The Sonar Maven plugin must be resolvable, either declared in the project's `pom.xml`/parent POM or available as a Maven plugin goal (`sonar:sonar`) from the configured Maven settings/repositories.
- `SONAR_PROJECT_ID`, `SONAR_URL`, and `SONAR_TOKEN` must be available (see the main `SKILL.md` for how to obtain these).

## Command

Run the analysis from the Maven project root (the directory containing the relevant `pom.xml`) using:

```bash
mvn verify sonar:sonar \
  -Dsonar.projectKey=<<SONAR_PROJECT_ID>> \
  -Dsonar.host.url=<<SONAR_URL>> \
  -Dsonar.login=<<SONAR_TOKEN>> \
  -DargLine="-XX:+EnableDynamicAgentLoading" \
  -Dsonar.qualitygate.wait=true
```

Substitute `<<SONAR_PROJECT_ID>>`, `<<SONAR_URL>>`, and `<<SONAR_TOKEN>>` with the actual values provided for the task. Do not omit any flag:

- `mvn verify` runs the full build lifecycle through `verify`, including tests and coverage instrumentation, before the `sonar:sonar` goal executes so coverage data is available to the analysis.
- `sonar:sonar` executes the SonarQube Maven plugin analysis and publishes results to the configured server.
- `-Dsonar.projectKey` identifies the project on the SonarQube server (`SONAR_PROJECT_ID`).
- `-Dsonar.host.url` points the analysis at the correct SonarQube server instance (`SONAR_URL`).
- `-Dsonar.login` authenticates the analysis publish call (`SONAR_TOKEN`).
- `-DargLine="-XX:+EnableDynamicAgentLoading"` passes the JVM flag needed for the JaCoCo/coverage agent to attach dynamically during the Surefire/Failsafe test run.
- `-Dsonar.qualitygate.wait=true` makes the Maven build block until the quality gate result is available and fail the build if the quality gate does not pass.

## Notes

- For multi-module Maven projects, run the command from the aggregator/root POM unless the task specifies a single module to analyze.
- Newer Sonar Maven plugin versions accept `-Dsonar.token=<<SONAR_TOKEN>>` as the preferred flag name instead of `-Dsonar.login`; use whichever flag the project's existing Sonar Maven plugin version and CI pipeline already use. Do not switch flag names arbitrarily if the project has an established convention.
- `SONAR_URL` reachability and `SONAR_TOKEN`/`SONAR_PROJECT_ID` validity are the first things to check if the Sonar goal itself fails (as opposed to a compile/test failure earlier in `verify`).
