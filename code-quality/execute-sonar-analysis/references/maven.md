# Execute SonarQube Analysis — Maven (Java)

## Prerequisites

- The target project must be a Maven project (a `pom.xml` must exist at the project root or module root).
- The Sonar Maven plugin must be resolvable, either declared in the project's `pom.xml`/parent POM or available as a Maven plugin goal (`sonar:sonar`) from the configured Maven settings/repositories.
- `mvn` must be available on `PATH`.
- `SONAR_PROJECT_ID`, `SONAR_URL`, and `SONAR_TOKEN` must be available as environment variables (see the main `SKILL.md` for how to obtain these).

## Preferred: Run via the script

Use [`../scripts/execute-sonar.sh`](../scripts/execute-sonar.sh) instead of typing the command below by hand. The script detects the `pom.xml` and runs the exact command documented in this file, with the same flags, deterministically:

```bash
SONAR_PROJECT_ID=<<SONAR_PROJECT_ID>> \
SONAR_URL=<<SONAR_URL>> \
SONAR_TOKEN=<<SONAR_TOKEN>> \
../scripts/execute-sonar.sh <<MAVEN_PROJECT_ROOT>>
```

This file documents what that script runs for a Maven project, so you can explain the command, troubleshoot a failure, or reproduce it manually if the script cannot be executed in the current environment.

## Underlying Command (what the script runs)

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

- For multi-module Maven projects, run the script (or the manual command) from the aggregator/root POM unless the task specifies a single module to analyze.
- Newer Sonar Maven plugin versions accept `-Dsonar.token=<<SONAR_TOKEN>>` as the preferred flag name instead of `-Dsonar.login`; use whichever flag the project's existing Sonar Maven plugin version and CI pipeline already use. If you need to switch flag names, update `scripts/execute-sonar.sh` rather than diverging between the script and this document.
- `SONAR_URL` reachability and `SONAR_TOKEN`/`SONAR_PROJECT_ID` validity are the first things to check if the Sonar goal itself fails (as opposed to a compile/test failure earlier in `verify`).
- `SONAR_EXTRA_ARGS` can be exported before running the script to append additional `-D` flags without editing the script.
