mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
mkfile_dir := $(dir $(mkfile_path))
ifeq ($(INPUT),)
INPUT := $(mkfile_dir)../input0.txt
endif

run: build
	@./a.out "$(INPUT)"

build: $(mkfile_dir)main.cpp
	@g++ -std=c++14 $<
