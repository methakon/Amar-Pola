cmake_minimum_required(VERSION 3.16)
project(madalasa_backend LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
add_compile_options(-Wall -Wextra -Wpedantic -Werror)

# Dependencies are built by backend/scripts/build_deps.sh; point CMAKE_PREFIX_PATH at its $PREFIX.
find_package(Drogon CONFIG REQUIRED)
enable_testing()

# Test-only header authentication. NEVER enable for a deployable build (see src/auth.h).
option(MA_SYNTHETIC_AUTH "Compile the synthetic test authenticator" OFF)
if(MA_SYNTHETIC_AUTH)
  add_compile_definitions(MA_SYNTHETIC_AUTH=1)
endif()

add_library(ma_core INTERFACE)
target_include_directories(ma_core INTERFACE src)
target_link_libraries(ma_core INTERFACE Drogon::Drogon)

add_executable(ma_backend src/main.cc)
target_link_libraries(ma_backend PRIVATE ma_core)

add_executable(test_core tests/cpp/test_core.cc)
target_link_libraries(test_core PRIVATE ma_core)
add_test(NAME core COMMAND test_core)
