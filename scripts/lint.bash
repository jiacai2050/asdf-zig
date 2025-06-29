#!/usr/bin/env bash

shellcheck --shell=bash --external-sources \
	bin/* --source-path=template/lib/ \
	lib/utils.bash \
	scripts/*

shfmt --language-dialect bash --diff \
	./**/*
