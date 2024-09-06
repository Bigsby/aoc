mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
mkfile_dir := $(dir $(mkfile_path))
class_name=Program

run: $(class_name).class
	@java -classpath $(mkfile_dir) $(class_name) $(INPUT)

Program.class: $(mkfile_dir)$(class_name).java
	@javac $<

.PHONY: run
