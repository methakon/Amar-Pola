cmake_minimum_required(VERSION 3.16)
project(madalasa_backend LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
add_compile_options(-Wall -Wextra -Wpedantic -Werror)

# Dependencies are built by backend/scripts/build_deps.sh; point CMAKE_PREFIX_PATH at its $PREFIX.
find_package(Drogon CONFIG REQUIRED)
find_package(OpenSSL 3.0 REQUIRED COMPONENTS Crypto)
find_package(CURL REQUIRED)
find_package(Threads REQUIRED)
enable_testing()

# Test-only header authentication. NEVER enable for a deployable build (see src/auth.h).
option(MA_SYNTHETIC_AUTH "Compile the synthetic test authenticator" OFF)


add_library(ma_core INTERFACE)
target_include_directories(ma_core INTERFACE src)
target_link_libraries(ma_core INTERFACE Drogon::Drogon)

add_executable(ma_backend src/main.cc)
add_library(ma_oidc src/google_oidc.cc src/google_jwks.cc)
target_include_directories(ma_oidc PUBLIC src)
target_link_libraries(ma_oidc PUBLIC Drogon::Drogon OpenSSL::Crypto PRIVATE CURL::libcurl Threads::Threads)
target_link_libraries(ma_backend PRIVATE ma_core ma_oidc)
if(MA_SYNTHETIC_AUTH)
  target_compile_definitions(ma_backend PRIVATE MA_SYNTHETIC_AUTH=1)
endif()

add_executable(test_core tests/cpp/test_core.cc)
target_link_libraries(test_core PRIVATE ma_core)
add_test(NAME core COMMAND test_core)

add_executable(test_oidc tests/cpp/test_oidc.cc)
target_link_libraries(test_oidc PRIVATE ma_oidc)
add_test(NAME oidc COMMAND test_oidc)
add_executable(test_jwks tests/cpp/test_jwks.cc)
target_link_libraries(test_jwks PRIVATE ma_oidc)
add_test(NAME jwks COMMAND test_jwks)
add_executable(test_jwks_fetch tests/cpp/test_jwks_fetch.cc)
target_link_libraries(test_jwks_fetch PRIVATE ma_oidc)
add_test(NAME jwks_fetch COMMAND test_jwks_fetch)
add_executable(test_oidc_http tests/cpp/test_oidc_http.cc)
target_link_libraries(test_oidc_http PRIVATE ma_core ma_oidc)
add_test(NAME oidc_http COMMAND test_oidc_http)
