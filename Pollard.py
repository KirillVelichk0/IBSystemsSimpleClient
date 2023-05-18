


def mod(a ,b):
	return a % b

def ExtendedGCD(a, b):
	'''Таки Кормен'''
	if b == 0:
		return a , 1, 0
	d1, x1, y1 = ExtendedGCD(b, mod(a, b) )
	d, x, y = d1, y1, x1 - (a//b)*y1
	return d, x, y


def EulerPhi(input):
	'''
		Функция Эйлера
		varphi(n), где n — натуральное число,
		равна количеству натуральных чисел,
		не больших n и взаимно простых с ним.
	'''
	res = 1
	i = 2
	while( i * i <= input):
		# пока i^2 <= input
		p = 1
		while(input % i == 0):
			input //= i 		# если не взаимно просты, делим
			p *= i			# произведение делителей i втч и кратных
		p //= i
		if ( p != 0 ):
			# если мы хоть раз делили на текущее i
			# то общее произведение делителей
			# умножаем на (i - 1)*i^(число раз - 1)
			res *= ( p * (i - 1))
		i += 1
	n = input - 1
	# input - уже изменен
	if(n == 0):
		return res
	else:
		# умножаем на (input - 1)*input^(число раз - 1)
		# но число раз = 1
		return n * res
	


def solve(g,a,p):
	# g**x = a mod p

	n = EulerPhi(p)
	'''
		использование Функции Эйлера дает возможность
		работать не только для простых p
	'''

	a1 = 0
	a2 = 0

	b1 = 0
	b2 = 0

	x1 = 1
	x2 = 1

	if(a == g):
		return (True , 1)

	start = True

	while(x1 != x2 or start):

		start = False

		'''
			Поиск совпадающих xi и x2i

			использован алгоритм
			похожий на этот
				http://en.wikipedia.org/wiki/Pollard%27s_rho_algorithm_for_logarithms
		'''

		'''
			xi ← f(xi-1),
			ai ← g(xi-1,ai-1),
			bi ← h(xi-1,bi-1)
		'''

		if(x1 < p//3):
			x1 = mod(a * x1, p)
			a1 = a1
			b1 = mod(b1 + 1, n)
		elif( x1 >= p//3 and x1 < 2*p//3):
			x1 = mod(x1 * x1, p)
			a1 = mod(2 * a1, n)
			b1 = mod(2 * b1, n)
		else: # (x1 >= 2*p/3)
			x1 = mod(g * x1, p)
			a1 = mod(a1 + 1, n)
			b1 = b1

		for i in range(2):

			'''
				x2i ← f(f(x2i-2)),
				a2i ← g(f(x2i-2),g(x2i-2,a2i-2)),
				b2i ← h(f(x2i-2),h(x2i-2,b2i-2))
			'''

			if(x2 < p//3):
				x2 = mod(a * x2, p)
				a2 = a2
				b2 = mod(b2 + 1, n)
			elif( x2 >= p//3 and x2 < 2*p//3):
				x2 = mod(x2 * x2, p)
				a2 = mod(2 * a2, n)
				b2 = mod(2 * b2, n)
			else: # (x2 >= 2*p/3)
				x2 = mod(g * x2, p)
				a2 = mod(a2 + 1, n)
				b2 = b2

	u = mod(a1 - a2, n)
	v = mod(b2 - b1, n)

	if( mod(v , n) == 0 ):
		return (False, None)
		'''
			В питоне можно возвращать
			не одно значение,
			а несколько
		'''

	d, nu, mu = ExtendedGCD(v , n)
	'''
		nu = v^(-1) mod n
	'''
	x = None
	i = 0
	while( i != (d + 1)):
		'''
			Это наименее эффективная реализация
			алгоритма Полларда,
			(в таком виде предложена самим Поллардом)

			g^u == a^v 				mod p
			g^(u*nu) = a^(v*nu)	 = a ^(d - n*nu) = a^(d) = g(x*d) 	mod p
			xd =  u * nu + w * n

			далее использован перебор,
			правда значительно меньшего размера
			чем в premutive_log

			Проблема в том, что нужно правильно подобрать w
		'''
		w = i
		x = (( u * nu + w * n )//d) % n
			# тут иcпользован % вместо mod()
		num = mod(pow(g, x, p) - mod(a, p), p)
		if( num == 0 ):
			return  (True, x)
		i += 1

	return (False, x)