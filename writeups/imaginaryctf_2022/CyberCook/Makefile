WABT_PATH=~/CTF/bin/wabt/
WABT_BUILD_PATH=out/clang/Debug
WASM_PATH=bin.wasm

_main.c:
	echo "int main(){}" > "_main.c"
wasm-rt.h:
	cp $(WABT_PATH)/wasm2c/wasm-rt.h ./
bin.c:
	$(WABT_PATH)/$(WABT_BUILD_PATH)/wasm2c $(WASM_PATH) -o bin.c

out: _main.c wasm-rt.h bin.c
	gcc -O2 -fno-optimize-sibling-calls -frounding-math -fsignaling-nans bin.c ~/CTF/bin/wabt/wasm2c/wasm-rt-impl.c _main.c -lm -o out
