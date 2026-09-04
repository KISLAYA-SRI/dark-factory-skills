# Dimension 4: Coverage (Unit Test Coverage) — Fix Patterns & Examples

## Overview

SonarQube measures **line coverage** and **branch coverage**. The quality gate typically requires 80%+ overall coverage. New code often requires higher thresholds (e.g., 85% on new code).

---

## Identifying Uncovered Code from SonarQube

1. In SonarQube UI → Project → **Coverage** tab.
2. Click on a file to see line-by-line coverage (green = covered, red = uncovered).
3. Branch coverage shows uncovered `if/else`, `switch`, ternary branches.
4. Use the SonarQube API to fetch uncovered lines programmatically:
   ```
   GET /api/measures/component?component={projectKey}&metricKeys=uncovered_lines,uncovered_conditions
   ```

---

## JaCoCo Configuration

```xml
<!-- pom.xml -->
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.11</version>
    <configuration>
        <excludes>
            <!-- Exclude generated code -->
            <exclude>**/*MapperImpl.class</exclude>      <!-- MapStruct -->
            <exclude>**/*_.class</exclude>               <!-- JPA metamodel -->
            <exclude>**/Q*.class</exclude>               <!-- QueryDSL -->
            <exclude>**/*Application.class</exclude>     <!-- Spring Boot main -->
            <exclude>**/config/**</exclude>              <!-- Config classes -->
            <exclude>**/dto/**</exclude>                 <!-- DTOs (POJOs) -->
            <exclude>**/entity/**</exclude>              <!-- JPA entities -->
            <exclude>**/exception/**</exclude>           <!-- Exception classes -->
        </excludes>
    </configuration>
    <executions>
        <execution>
            <id>prepare-agent</id>
            <goals><goal>prepare-agent</goal></goals>
        </execution>
        <execution>
            <id>report</id>
            <phase>test</phase>
            <goals><goal>report</goal></goals>
        </execution>
        <execution>
            <id>check</id>
            <goals><goal>check</goal></goals>
            <configuration>
                <rules>
                    <rule>
                        <element>BUNDLE</element>
                        <limits>
                            <limit>
                                <counter>LINE</counter>
                                <value>COVEREDRATIO</value>
                                <minimum>0.80</minimum>
                            </limit>
                            <limit>
                                <counter>BRANCH</counter>
                                <value>COVEREDRATIO</value>
                                <minimum>0.75</minimum>
                            </limit>
                        </limits>
                    </rule>
                </rules>
            </configuration>
        </execution>
    </executions>
</plugin>
```

---

## Excluding Generated Code from Coverage

For MapStruct mappers, Lombok-generated code, and JPA entities:

```java
// Option 1: @Generated annotation on the class
@Generated("mapstruct")
public class UserMapperImpl implements UserMapper { ... }

// Option 2: sonar-project.properties exclusions
// sonar.coverage.exclusions=**/mapper/**/*MapperImpl.java,**/entity/**,**/dto/**

// Option 3: JaCoCo excludes in pom.xml (shown above)
```

---

## Writing Unit Tests — JUnit 5 + Mockito

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private UserMapper userMapper;

    @InjectMocks
    private UserService userService;

    @Test
    @DisplayName("Should return user DTO when user exists")
    void getUserById_whenUserExists_returnsDto() {
        // Arrange
        Long userId = 1L;
        User user = User.builder().id(userId).name("Alice").build();
        UserDto expectedDto = new UserDto(userId, "Alice");

        when(userRepository.findById(userId)).thenReturn(Optional.of(user));
        when(userMapper.toDto(user)).thenReturn(expectedDto);

        // Act
        UserDto result = userService.getUserById(userId);

        // Assert
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(userId);
        assertThat(result.getName()).isEqualTo("Alice");
        verify(userRepository).findById(userId);
    }

    @Test
    @DisplayName("Should throw ResourceNotFoundException when user not found")
    void getUserById_whenUserNotFound_throwsException() {
        // Arrange
        Long userId = 99L;
        when(userRepository.findById(userId)).thenReturn(Optional.empty());

        // Act + Assert
        assertThatThrownBy(() -> userService.getUserById(userId))
            .isInstanceOf(ResourceNotFoundException.class)
            .hasMessageContaining("99");
    }

    @Test
    @DisplayName("Should cover both branches of conditional logic")
    void processUser_coversBothBranches() {
        // Test branch 1: active user
        User activeUser = User.builder().status(UserStatus.ACTIVE).build();
        assertThat(userService.canLogin(activeUser)).isTrue();

        // Test branch 2: inactive user
        User inactiveUser = User.builder().status(UserStatus.INACTIVE).build();
        assertThat(userService.canLogin(inactiveUser)).isFalse();
    }
}
```

---

## Testing Reactive Code (Mono/Flux)

```java
@ExtendWith(MockitoExtension.class)
class ReactiveUserServiceTest {

    @Mock
    private ReactiveUserRepository userRepository;

    @InjectMocks
    private ReactiveUserService userService;

    @Test
    void getUserById_whenExists_returnsUser() {
        User user = new User(1L, "Alice");
        when(userRepository.findById(1L)).thenReturn(Mono.just(user));

        StepVerifier.create(userService.getUserById(1L))
            .expectNextMatches(dto -> dto.getName().equals("Alice"))
            .verifyComplete();
    }

    @Test
    void getUserById_whenNotFound_emitsError() {
        when(userRepository.findById(99L)).thenReturn(Mono.empty());

        StepVerifier.create(userService.getUserById(99L))
            .expectError(ResourceNotFoundException.class)
            .verify();
    }

    @Test
    void getAllUsers_returnsFluxOfUsers() {
        List<User> users = List.of(new User(1L, "Alice"), new User(2L, "Bob"));
        when(userRepository.findAll()).thenReturn(Flux.fromIterable(users));

        StepVerifier.create(userService.getAllUsers())
            .expectNextCount(2)
            .verifyComplete();
    }

    @Test
    void processUser_onError_emitsFallback() {
        when(userRepository.findById(1L))
            .thenReturn(Mono.error(new DataAccessException("DB down") {}));

        StepVerifier.create(userService.getUserById(1L))
            .expectError(ServiceException.class)
            .verify();
    }
}
```

---

## Coverage Strategy for Uncovered Lines

1. **Identify uncovered lines**: Use SonarQube UI or JaCoCo HTML report at `target/site/jacoco/index.html`.
2. **Prioritize by risk**: Cover service layer > controller layer > repository layer.
3. **Cover all branches**: For each `if/else`, write at least one test per branch.
4. **Exception paths**: Write tests that trigger each `catch` block and `throw` statement.
5. **Null/empty inputs**: Test with `null`, empty strings, empty lists.
6. **Edge cases**: Test boundary values (0, -1, MAX_VALUE, empty string, etc.).

---

## Coverage Thresholds by Layer

| Layer | Recommended Coverage |
|---|---|
| Service (business logic) | 90%+ |
| Controller (REST endpoints) | 80%+ |
| Repository (custom queries) | 70%+ |
| Utility/Helper classes | 85%+ |
| Generated code (MapStruct, Lombok) | Exclude |
| Configuration classes | Exclude |
