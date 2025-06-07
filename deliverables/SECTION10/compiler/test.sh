#!/usr/bin/bash
# coding: utf-8

# python3 JackAnalyzer.py ./Square.jack
# cat Square.xml

echo "ArrayTest------------------------------"
python3 JackAnalyzer.py ../assets/ArrayTest 2> /dev/null
python3 ediff.py ./ArrayTest/Main.xml.dest ./Main.xml

echo

echo "ExpressionLessSquare-------------------"
python3 JackAnalyzer.py ../assets/ExpressionLessSquare 2> /dev/null
python3 ediff.py ./ExpressionLessSquare/Main.xml.dest ./Main.xml
python3 ediff.py ./ExpressionLessSquare/Square.xml.dest ./Square.xml
python3 ediff.py ./ExpressionLessSquare/SquareGame.xml.dest ./SquareGame.xml 

echo 

echo "Square---------------------------------"
python3 JackAnalyzer.py ../assets/Square 2> /dev/null
python3 ediff.py ./Square/Main.xml.dest ./Main.xml
python3 ediff.py ./Square/Square.xml.dest ./Square.xml
python3 ediff.py ./Square/SquareGame.xml.dest ./SquareGame.xml 

rm *.xml

# EOF
