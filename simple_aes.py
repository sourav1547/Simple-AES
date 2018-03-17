s_box = {'0000':'1001', '0001':'0100', '0010':'1010', '0011':'1011', '0100':'1101', '0101':'0001', '0110':'0101', '0111':'0101', '1000':'0110', '1001':'0010', '1010':'0000', '1011':'0011', '1100':'1100', '1101':'1110', '1110':'1111', '1111':'0111'}

def rotNib(_nibbles):
	nibble1 = _nibbles[0:4]
	nibble2 = _nibbles[4:8]
	return nibble2+nibble1

def subNib(_nibbles):
	nibble1 = _nibbles[0:4]
	nibble2 = _nibbles[4:8]
	return s_box[nibble1]+s_box[nibble2]


def generate_keys(master_key):
	
	w0 = master_key[0:8]
	# print 'w0',w0

	w1 = master_key[8:16]
	# print 'w1',w1


	w2_temp = (int(w0,2)^int('10000000',2))^int(subNib(rotNib(w1)),2);
	w2 = '{0:0{1}b}'.format(w2_temp,w_len)
	# print 'w2',w2


	w3_temp = int(w2,2)^int(w1,2)
	w3 = '{0:0{1}b}'.format(w3_temp,w_len)
	# print 'w3',w3


	w4_temp = int(w2,2)^int('00110000',2)^int(subNib(rotNib(w3)),2)
	w4 = '{0:0{1}b}'.format(w4_temp,w_len)
	# print 'w4',w4


	w5_temp = int(w4,2)^int(w3,2)
	w5 =  '{0:0{1}b}'.format(w5_temp,w_len)
	# print 'w5',w5


	key0 = w0+w1
	key1 = w2+w3
	key2 = w4+w5

	return (key0, key1, key2);

	print 'k0', key0
	print 'k1', key1
	print 'k2', key2


def roundOne(input,key1):
	n1 = input[0:4]
	n2 = input[4:8]
	n3 = input[8:12]
	n4 = input[12:16]

	r1 = s_box[n1]
	r2 = s_box[n2]
	r3 = s_box[n3]
	r4 = s_box[n4]

	# output = r1+r4+r3+r2

	mul_out = '1111011000110011'

	re_temp = int(mul_out,2)^int(key1,2);
	return '{0:0{1}b}'.format(re_temp,w_len*2)

def roundTwo(input, key2):
	r1 = s_box[input[0:4]]
	r2 = s_box[input[4:8]]
	r3 = s_box[input[8:12]]
	r4 = s_box[input[12:16]]

	temp_out = r1+r4+r3+r2;
	re_temp = int(temp_out,2)^int(key2,2);
	return '{0:0{1}b}'.format(re_temp,w_len*2)


	

def encrypt(plain_text, key1, key2):
	output1 = roundOne(plain_text,key1)
	output2 = roundTwo(output1, key2)
	return output2



def decrypt(c_text, key0, key1, key2):



w_len = 8
if __name__=='__main__':

	master_key = '0100101011110101'
	plain_text = '1101011100101000'

	keys = generate_keys(key)

	key0 = keys[0]
	key1 = keys[1]
	key2 = keys[2]


	re_temp = int(plain_text,2)^int(key0,2)
	input1 = '{0:0{1}b}'.format(re_temp,w_len*2)

	c_text = encrypt(input1, key1, key2)
	print c_text


	