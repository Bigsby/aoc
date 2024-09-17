mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
mkfile_dir := $(dir $(mkfile_path))
class_name=program

run: $(mkfile_dir)$(class_name).jar
	@java -jar $< $(INPUT)

$(mkfile_dir)$(class_name).jar: $(mkfile_dir)$(class_name).kt
	@kotlinc $< -include-runtime -d $@ 

.PHONY: run
