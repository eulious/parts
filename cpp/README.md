ビルド
```sh
$ cmake -S . -B build
$ cmake --build build -v --clean-first
$ ./build/test/a.out
```

テスト
```sh
$ cd build
$ ctest .
```
