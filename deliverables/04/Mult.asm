@2
M=0
@1
D=M
@i_addr
M=D
(LOOP)
@i_addr
D=M-1
@END
D;JLT // if ( i - R1 ) > 0 then GOTO END -> ( i - R1 ) <=0 then cotinue
@0    // R0
D=M
@2
M=D+M
@i_addr
M=M-1
@LOOP
0;JMP
(END)
@END
0;JMP



	
	
	
