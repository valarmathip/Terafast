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
include examples/CMakeFiles/amqp_consumer.dir/depend.make

# Include the progress variables for this target.
include examples/CMakeFiles/amqp_consumer.dir/progress.make

# Include the compile flags for this target's objects.
include examples/CMakeFiles/amqp_consumer.dir/flags.make

examples/CMakeFiles/amqp_consumer.dir/amqp_consumer.c.o: examples/CMakeFiles/amqp_consumer.dir/flags.make
examples/CMakeFiles/amqp_consumer.dir/amqp_consumer.c.o: ../examples/amqp_consumer.c
	$(CMAKE_COMMAND) -E cmake_progress_report /home/gkrishnan/ndpi/rabbitmq-c-master/build/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building C object examples/CMakeFiles/amqp_consumer.dir/amqp_consumer.c.o"
	cd /home/gkrishnan/ndpi/rabbitmq-c-master/build/examples && /usr/bin/gcc  $(C_DEFINES) $(C_FLAGS) -o CMakeFiles/amqp_consumer.dir/amqp_consumer.c.o   -c /home/gkrishnan/ndpi/rabbitmq-c-master/examples/amqp_consumer.c

examples/CMakeFiles/amqp_consumer.dir/amqp_consumer.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/amqp_consumer.dir/amqp_consumer.c.i"
	cd /home/gkrishnan/ndpi/rabbitmq-c-master/build/examples && /usr/bin/gcc  $(C_DEFINES) $(C_FLAGS) -E /home/gkrishnan/ndpi/rabbitmq-c-master/examples/amqp_consumer.c > CMakeFiles/amqp_consumer.dir/amqp_consumer.c.i

examples/CMakeFiles/amqp_consumer.dir/amqp_consumer.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/amqp_consumer.dir/amqp_consumer.c.s"
	cd /home/gkrishnan/ndpi/rabbitmq-c-master/build/examples && /usr/bin/gcc  $(C_DEFINES) $(C_FLAGS) -S /home/gkrishnan/ndpi/rabbitmq-c-master/examples/amqp_consumer.c -o CMakeFiles/amqp_consumer.dir/amqp_consumer.c.s

examples/CMakeFiles/amqp_consumer.dir/amqp_consumer.c.o.requires:
.PHONY : examples/CMakeFiles/amqp_consumer.dir/amqp_consumer.c.o.requires

examples/CMakeFiles/amqp_consumer.dir/amqp_consumer.c.o.provides: examples/CMakeFiles/amqp_consumer.dir/amqp_consumer.c.o.requires
	$(MAKE) -f examples/CMakeFiles/amqp_consumer.dir/build.make examples/CMakeFiles/amqp_consumer.dir/amqp_consumer.c.o.provides.build
.PHONY : examples/CMakeFiles/amqp_consumer.dir/amqp_consumer.c.o.provides

examples/CMakeFiles/amqp_consumer.dir/amqp_consumer.c.o.provides.build: examples/CMakeFiles/amqp_consumer.dir/amqp_consumer.c.o

examples/CMakeFiles/amqp_consumer.dir/utils.c.o: examples/CMakeFiles/amqp_consumer.dir/flags.make
examples/CMakeFiles/amqp_consumer.dir/utils.c.o: ../examples/utils.c
	$(CMAKE_COMMAND) -E cmake_progress_report /home/gkrishnan/ndpi/rabbitmq-c-master/build/CMakeFiles $(CMAKE_PROGRESS_2)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building C object examples/CMakeFiles/amqp_consumer.dir/utils.c.o"
	cd /home/gkrishnan/ndpi/rabbitmq-c-master/build/examples && /usr/bin/gcc  $(C_DEFINES) $(C_FLAGS) -o CMakeFiles/amqp_consumer.dir/utils.c.o   -c /home/gkrishnan/ndpi/rabbitmq-c-master/examples/utils.c

examples/CMakeFiles/amqp_consumer.dir/utils.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/amqp_consumer.dir/utils.c.i"
	cd /home/gkrishnan/ndpi/rabbitmq-c-master/build/examples && /usr/bin/gcc  $(C_DEFINES) $(C_FLAGS) -E /home/gkrishnan/ndpi/rabbitmq-c-master/examples/utils.c > CMakeFiles/amqp_consumer.dir/utils.c.i

examples/CMakeFiles/amqp_consumer.dir/utils.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/amqp_consumer.dir/utils.c.s"
	cd /home/gkrishnan/ndpi/rabbitmq-c-master/build/examples && /usr/bin/gcc  $(C_DEFINES) $(C_FLAGS) -S /home/gkrishnan/ndpi/rabbitmq-c-master/examples/utils.c -o CMakeFiles/amqp_consumer.dir/utils.c.s

examples/CMakeFiles/amqp_consumer.dir/utils.c.o.requires:
.PHONY : examples/CMakeFiles/amqp_consumer.dir/utils.c.o.requires

examples/CMakeFiles/amqp_consumer.dir/utils.c.o.provides: examples/CMakeFiles/amqp_consumer.dir/utils.c.o.requires
	$(MAKE) -f examples/CMakeFiles/amqp_consumer.dir/build.make examples/CMakeFiles/amqp_consumer.dir/utils.c.o.provides.build
.PHONY : examples/CMakeFiles/amqp_consumer.dir/utils.c.o.provides

examples/CMakeFiles/amqp_consumer.dir/utils.c.o.provides.build: examples/CMakeFiles/amqp_consumer.dir/utils.c.o

examples/CMakeFiles/amqp_consumer.dir/unix/platform_utils.c.o: examples/CMakeFiles/amqp_consumer.dir/flags.make
examples/CMakeFiles/amqp_consumer.dir/unix/platform_utils.c.o: ../examples/unix/platform_utils.c
	$(CMAKE_COMMAND) -E cmake_progress_report /home/gkrishnan/ndpi/rabbitmq-c-master/build/CMakeFiles $(CMAKE_PROGRESS_3)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building C object examples/CMakeFiles/amqp_consumer.dir/unix/platform_utils.c.o"
	cd /home/gkrishnan/ndpi/rabbitmq-c-master/build/examples && /usr/bin/gcc  $(C_DEFINES) $(C_FLAGS) -o CMakeFiles/amqp_consumer.dir/unix/platform_utils.c.o   -c /home/gkrishnan/ndpi/rabbitmq-c-master/examples/unix/platform_utils.c

examples/CMakeFiles/amqp_consumer.dir/unix/platform_utils.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/amqp_consumer.dir/unix/platform_utils.c.i"
	cd /home/gkrishnan/ndpi/rabbitmq-c-master/build/examples && /usr/bin/gcc  $(C_DEFINES) $(C_FLAGS) -E /home/gkrishnan/ndpi/rabbitmq-c-master/examples/unix/platform_utils.c > CMakeFiles/amqp_consumer.dir/unix/platform_utils.c.i

examples/CMakeFiles/amqp_consumer.dir/unix/platform_utils.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/amqp_consumer.dir/unix/platform_utils.c.s"
	cd /home/gkrishnan/ndpi/rabbitmq-c-master/build/examples && /usr/bin/gcc  $(C_DEFINES) $(C_FLAGS) -S /home/gkrishnan/ndpi/rabbitmq-c-master/examples/unix/platform_utils.c -o CMakeFiles/amqp_consumer.dir/unix/platform_utils.c.s

examples/CMakeFiles/amqp_consumer.dir/unix/platform_utils.c.o.requires:
.PHONY : examples/CMakeFiles/amqp_consumer.dir/unix/platform_utils.c.o.requires

examples/CMakeFiles/amqp_consumer.dir/unix/platform_utils.c.o.provides: examples/CMakeFiles/amqp_consumer.dir/unix/platform_utils.c.o.requires
	$(MAKE) -f examples/CMakeFiles/amqp_consumer.dir/build.make examples/CMakeFiles/amqp_consumer.dir/unix/platform_utils.c.o.provides.build
.PHONY : examples/CMakeFiles/amqp_consumer.dir/unix/platform_utils.c.o.provides

examples/CMakeFiles/amqp_consumer.dir/unix/platform_utils.c.o.provides.build: examples/CMakeFiles/amqp_consumer.dir/unix/platform_utils.c.o

# Object files for target amqp_consumer
amqp_consumer_OBJECTS = \
"CMakeFiles/amqp_consumer.dir/amqp_consumer.c.o" \
"CMakeFiles/amqp_consumer.dir/utils.c.o" \
"CMakeFiles/amqp_consumer.dir/unix/platform_utils.c.o"

# External object files for target amqp_consumer
amqp_consumer_EXTERNAL_OBJECTS =

examples/amqp_consumer: examples/CMakeFiles/amqp_consumer.dir/amqp_consumer.c.o
examples/amqp_consumer: examples/CMakeFiles/amqp_consumer.dir/utils.c.o
examples/amqp_consumer: examples/CMakeFiles/amqp_consumer.dir/unix/platform_utils.c.o
examples/amqp_consumer: librabbitmq/librabbitmq.so.4.1.4
examples/amqp_consumer: /usr/lib/i386-linux-gnu/libssl.so
examples/amqp_consumer: /usr/lib/i386-linux-gnu/libcrypto.so
examples/amqp_consumer: examples/CMakeFiles/amqp_consumer.dir/build.make
examples/amqp_consumer: examples/CMakeFiles/amqp_consumer.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking C executable amqp_consumer"
	cd /home/gkrishnan/ndpi/rabbitmq-c-master/build/examples && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/amqp_consumer.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
examples/CMakeFiles/amqp_consumer.dir/build: examples/amqp_consumer
.PHONY : examples/CMakeFiles/amqp_consumer.dir/build

examples/CMakeFiles/amqp_consumer.dir/requires: examples/CMakeFiles/amqp_consumer.dir/amqp_consumer.c.o.requires
examples/CMakeFiles/amqp_consumer.dir/requires: examples/CMakeFiles/amqp_consumer.dir/utils.c.o.requires
examples/CMakeFiles/amqp_consumer.dir/requires: examples/CMakeFiles/amqp_consumer.dir/unix/platform_utils.c.o.requires
.PHONY : examples/CMakeFiles/amqp_consumer.dir/requires

examples/CMakeFiles/amqp_consumer.dir/clean:
	cd /home/gkrishnan/ndpi/rabbitmq-c-master/build/examples && $(CMAKE_COMMAND) -P CMakeFiles/amqp_consumer.dir/cmake_clean.cmake
.PHONY : examples/CMakeFiles/amqp_consumer.dir/clean

examples/CMakeFiles/amqp_consumer.dir/depend:
	cd /home/gkrishnan/ndpi/rabbitmq-c-master/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/gkrishnan/ndpi/rabbitmq-c-master /home/gkrishnan/ndpi/rabbitmq-c-master/examples /home/gkrishnan/ndpi/rabbitmq-c-master/build /home/gkrishnan/ndpi/rabbitmq-c-master/build/examples /home/gkrishnan/ndpi/rabbitmq-c-master/build/examples/CMakeFiles/amqp_consumer.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : examples/CMakeFiles/amqp_consumer.dir/depend

