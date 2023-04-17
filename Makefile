
.PHONY: ex1 ex2 ex3 ex4

ex1:
	sudo mn --custom ./topologia01.py --topo mytopo --link tc --test ex01
ex2:
	sudo mn --custom ./topologia01.py --topo mytopo --link tc --test ex02
ex3:
	sudo mn --custom ./topologia02.py --nat --topo tree,1,4 --link tc --test ex03
ex4:
	sudo mn --custom ./topologia03.py --topo mytopo --link tc --test ex04