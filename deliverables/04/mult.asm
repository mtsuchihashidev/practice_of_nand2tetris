// Multi
@i
M=0
@R2
M=0
(Loop)
@i
D=M
@R1
D=D-M
@End
D;JGE
@R0
D=M
@R2
M=D+M
@i
M=M+1
@Loop
0;JMP
(End)