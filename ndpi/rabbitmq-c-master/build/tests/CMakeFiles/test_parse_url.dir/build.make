# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 2.8

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list

# Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/gkrishnan/ndpi/rabbitmq-c-master

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/gkrishnan/ndpi/rabbitmq-c-master/build

# Include any dependencies generated for this target.
include tests/CMakeFiles/test_parse_url.dir/depend.make

# Include the progress variables for this target.
include tests/CMakeFiles/test_parse_url.dir/progress.make

# Include the compile flags for this target's objects.
include tests/CMakeFiles/test_parse_url.dir/flags.make

tests/CMakeFiles/test_parse_url.dir/test_parse_url.c.o: tests/CMakeFiles/test_parse_url.dir/flags.make
tests/CMakeFiles/test_parse_url.dir/test_parse_url.c.o: ../tests/test_parse_url.c
	$(CMAKE_COMMAND) -E cmake_progress_report /home/gkrishnan/ndpi/rabbitmq-c-master/build/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building C object tests/CMakeFiles/test_parse_url.dir/test_parse_url.c.o"
	cd /home/gkrishnan/ndpi/rabbitmq-c-master/build/tests && /usr/bin/gcc  $(C_DEFINES) $(C_FLAGS) -o CMakeFiles/test_parse_url.dir/test_parse_url.c.o   -c /home/gkrishnan/ndpi/rabbitmq-c-master/tests/test_parse_url.c

tests/CMakeFiles/test_parse_url.dir/test_parse_url.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/test_parse_url.dir/test_parse_url.c.i"
	cd /home/gkrishnan/ndpi/rabbitmq-c-master/build/tests && /usr/bin/gcc  $(C_DEFINES) $(C_FLAGS) -E /home/gkrishnan/ndpi/rabbitmq-c-master/tests/test_parse_url.c > CMakeFiles/test_parse_url.dir/test_parse_url.c.i

tests/CMakeFiles/test_parse_url.dir/test_parse_url.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/test_parse_url.dir/test_parse_url.c.s"
	cd /home/gkrishnan/ndpi/rabbitmq-c-master/build/tests && /usr/bin/gcc  $(C_DEFINES) $(C_FLAGS) -S /home/gkrishnan/ndpi/rabbitmq-c-master/tests/test_parse_url.c -o CMakeFiles/test_parse_url.dir/test_parse_url.c.s

tests/CMakeFiles/test_parse_url.dir/test_parse_url.c.o.requires:
.PHONY : tests/CMakeFiles/test_parse_url.dir/test_parse_url.c.o.requires

tests/CMakeFiles/test_parse_url.dir/test_parse_url.c.o.provides: tests/CMakeFiles/test_parse_url.dir/test_parse_url.c.o.requires
	$(MAKE) -f tests/CMakeFiles/test_parse_url.dir/build.make tests/CMakeFiles/test_parse_url.dir/test_parse_url.c.o.provides.build
.PHONY : tests/CMakeFiles/test_parse_url.dir/test_parse_url.c.o.provides

tests/CMakeFiles/test_parse_url.dir/test_parse_url.c.o.provides.build: tests/CMakeFiles/test_parse_url.dir/test_parse_url.c.o

# Object files for target test_parse_url
test_parse_url_OBJECTS = \
"CMakeFiles/test_parse_url.dir/test_parse_url.c.o"

# External object files for target test_parse_url
test_parse_url_EXTERNAL_OBJECTS =

tests/test_parse_url: tests/CMakeFiles/test_parse_url.dir/test_parse_url.c.o
tests/test_parse_url: librabbitmq/librabbitmq.a
tests/test_parse_url: /usr/lib/i386-linux-gnu/libssl.so
tests/test_parse_url: /usr/lib/i386-linux-gnu/libcrypto.so
tests/test_parse_url: tests/CMakeFiles/test_parse_url.dir/build.make
tests/test_parse_url: tests/CMakeFiles/test_parse_url.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking C executable test_parse_url"
	cd /home/gkrishnan/ndpi/rabbitmq-c-master/build/tests && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/test_parse_url.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
tests/CMakeFiles/test_parse_url.dir/build: tests/test_parse_url
.PHONY : tests/CMakeFiles/test_parse_url.dir/build

tests/CMakeFiles/test_parse_url.dir/requires: tests/CMakeFiles/test_parse_url.dir/test_parse_url.c.o.requires
.PHONY : tests/CMakeFiles/test_parse_url.dir/requires

tests/CMakeFiles/test_parse_url.dir/clean:
	cd /home/gkrishnan/ndpi/rabbitmq-c-master/build/tests && $(CMAKE_COMMAND) -P CMakeFiles/test_parse_url.dir/cmake_clean.cmake
.PHONY : tests/CMakeFiles/test_parse_url.dir/clean

tests/CMakeFiles/test_parse_url.dir/depend:
	cd /home/gkrishnan/ndpi/rabbitmq-c-master/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/gkrishnan/ndpi/rabbitmq-c-master /home/gkrishnan/ndpi/rabbitmq-c-master/tests /home/gkrishnan/ndpi/rabbitmq-c-master/build /home/gkrishnan/ndpi/rabbitmq-c-master/build/tests /home/gkrishnan/ndpi/rabbitmq-c-master/build/tests/CMakeFiles/test_parse_url.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : tests/CMakeFiles/test_parse_url.dir/depend

