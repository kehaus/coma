




class A(object):
	pass

class B(A):
	pass

class C(B):
	pass


print('herereer')



def f(x, y, a=1, b=3, c=5):
	print('x :', x)
	print('y :', y)
	print('a :', a)
	print('b :', b)
	print('c :', c)
	return 'x:{0:d}, y:{1:d}, a:{2:d}, b:{3:d}, c:{4:d}'.format(x,y,a,b,c)


prm = {'a': 41, 'b': 42, 'c': 43}
prm2 = {'a': 410, 'b': 420, 'c': 430}


s = f(11, 22, **prm)



def wrapper1(surrounding):

	def surround_with(word):
		return '{}{}{}'.format(surrounding, word, surrounding)
	return surround_with


def gen_f(f, **kwargs):
	def wrapper(*args):
		return f(*args, **kwargs)

	return wrapper



