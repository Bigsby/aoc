mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
mkfile_dir := $(dir $(mkfile_path))
ifeq ($(INPUT),)
INPUT := $(mkfile_dir)../input.txt
endif

run: build
	@./a.out "$(INPUT)"
	@rm ./a.out

build: $(mkfile_dir)run.cpp
	@g++ $<