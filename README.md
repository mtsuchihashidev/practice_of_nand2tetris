<head>
	<meta charset="UTF-8" />
</head>

# practice_of_nand2tetris

## TL;DR

* 実施していったNand2Tetrisの演習問題の解答を上げてく
* 個人的な気づきとかも書けたら書いていく
* 期限は設けないし気にしない。終わらせること、そしてなにより楽しむことを忘れない。

## Motivation

自作PCとかではなく、本当にコンピュータをゼロから作っていく。
情報科学系の基礎の基礎から身につけていく。

## 参照

### 部品一覧

#### NAND

```
回路名     Nand
入力       a, b
出力       out
関数       if a=b=1 then out=0 else out=1
コメント   このゲートは基本要素として使うため、実装する必要はない
```

#### NOT

```
回路名     Not
入力       in 
出力       out
関数       if in=0 then out=1 else out=0
コメント   -
```

#### OR

```
回路名     Or
入力       a, b
出力       out
関数       if a=b=0 then out=0 else out=1
コメント   -
```

#### AND

```
回路名     And
入力       a, b
出力       out
関数       if a=b=1 then out=1 else out=0
コメント   -
```

#### XOR

```
回路名     Xor
入力       a, b
出力       out
関数       if a!=b then out=1 else out=0
コメント   -
```

#### MUX

```
回路名     Mux
入力       a, b, sel
出力       out
関数       if sel=0 then out=a else out=b
コメント   -
```

#### DMUX

```
回路名     DMux
入力       in, sel
出力       a, b
関数       if sel=0 then {a=in, b=0} else {a=0, b=in}
コメント   -
```

#### NOT16

```
回路名     Not16
入力       in[16] // 16ビットのピン
出力       out[16]
関数       For i=0..15 out[i]=Not(in[i])
コメント   -
```

#### OR16

```
回路名     Or16
入力       a[16], b[16]
出力       out[16]
関数       For i=0..15 out[i]=Or(a[i], b[i])
コメント   -
```

#### AND16

```
回路名     And16
入力       a[16], b[16]
出力       out[16]
関数       For i=0..15 out[i]=And(a[i], b[i])
コメント   -
```

#### MUX16

```
回路名     Mux16
入力       a[16], b[16], sel
出力       out[16]
関数       If sel=0 then for i=0..15 out[i]=a[i]
           else for i=0..15 out[i]=b[i]
コメント   -
```

#### OR8WAY

```
回路名     Or8Way
入力       in[8]
出力       out
関数       out=Or(in[0], in[1],...,in[7])
コメント   -
```

#### MUX4WAY16

```
回路名     Mux4Way16
入力       a[16], b[16], c[16], d[16], sel[2]
出力       out[16]
関数       If sel=00 then out=a else if sel=01 then out=b
           else if sel=10 then out=c else if sel=11 then out=d
コメント   代入操作はすべて16ビットに対して行われる。たとえば、「out=a」は
          「for i=0..15 out[i]=a[i]」を意味する。
```

| sel[1] | sel[0] | out   |
|:------:|:------:|:-----:|
|    0   |    0   |   a   |
|    0   |    1   |   b   |
|    1   |    0   |   c   |
|    1   |    1   |   d   |

#### MUX8WAY16

```
回路名     Mux4Way16
入力       a[16],b[16],c[16],d[16],e[16],f[16],g[16],h[16],sel[3]
出力       out[16]
関数       If sel=000 then out=a else if sel=001 then out=b
           else if sel=010 then out=c ... else if sel=111 then out=h
コメント   -
```

#### DMUX4WAY16

```
回路名     DMux4Way16
入力       in, sel[2]
出力       a, b, c, d
関数       If sel=00 then {a=in, b=c=d=0}
           else if sel=01 then {b=in, a=c=d=0}
		   else if sel=10 then {c=in, a=b=d=0}
		   else if sel=11 then {d=in, a=b=c=0}
コメント   -
```

| sel[1] | sel[0] |   a  |   b  |   c  |   d  |
|:------:|:------:|:----:|:----:|:----:|:----:|
|    0   |    0   |  in  |   0  |   0  |   0  |
|    0   |    1   |   0  |  in  |   0  |   0  |
|    1   |    0   |   0  |   0  |  in  |   0  |
|    1   |    1   |   0  |   0  |   0  |  in  |

#### DMUX8WAY16

```
回路名     DMux8Way16
入力       in, sel[3]
出力       a, b, c, d, e, f, g, h
関数       If sel=000 then {a=in, b=c=d=e=f=g=h=0}
           else if sel=001 then {b=in, a=c=d=e=f=g=h=0}
		   else if sel=010 ...
		    ...
		   else if sel=111 then {h=in, a=b=c=d=e=f=g=h=0}
コメント   -
```

#### ADD16

```
回路名     Add16
入力       a[16], b[16]
出力       out[16]
関数       out = a + b
コメント   ２の補数による加算。
           オーバフローは検出されない。
```

#### INC16

```
回路名     Inc16
入力       in[16]
出力       out[16]
関数       out = in + 1
コメント   ２の補数による加算。
           オーバフローは検出されない。
```

#### ALU

```
回路名     ALU
入力       x[16], y[16], // ふたつの16ビットデータ入力
           zx, // 入力ｘをゼロにする
		   nx, // 入力ｘを反転（negate）する
		   zy, // 入力ｙをゼロにする
		   ny, // 入力ｙを反転（negate）する
		   f,  // 関数コード：１は「加算」、０は「Ａｎｄ演算」に対応する
		   no  // 出力outを反転する
出力       out[16], // １６ビットの出力
           zr,      // out=0の場合にのみTrue
		   ng       // out<0の場合にのみTrue
関数       if zx then x = 0      // １６ビットの定数ゼロ
           if nx then x = !x     // ビット単位の反転
		   if zy then y = 0      // １６ビットの定数ゼロ
		   if ny then y = !y     // ビット単位の反転
		   if f then out = x + y // ２の補数による加算
		        else out = x & y // ビット単位のAnd演算
		   if no then out = !out // ビット単位の反転
		   if out=0 then zr = 1 else zr = 0 // １６ビットの等号比較
		   if out<0 then ng = 1 else ng = 0 // １６ビットの負判定
コメント   オーバフローは検出されない。
```


