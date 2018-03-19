import sys

s_box = {'0000':'1001', '0001':'0100', '0010':'1010', '0011':'1011', '0100':'1101', '0101':'0001', '0110':'1000', '0111':'0101', '1000':'0110', '1001':'0010', '1010':'0000', '1011':'0011', '1100':'1100', '1101':'1110', '1110':'1111', '1111':'0111'}

s_inv = {'1000':'0110', '0101':'0111', '1001':'0000', '0100':'0001', '1011':'0011', '1010':'0010', '0001':'0101', '1101':'0100', '0111':'1111', '1111':'1110', '1100':'1100', '1110':'1101', '0000':'1010', '0011':'1011', '0010':'1001', '0110':'1000'}

s_mul = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15],
		[0, 2, 4, 6, 8,10,12,14, 3, 1, 7, 5,11, 9,15,13],
		[0, 3, 6, 5,12,15,10, 9,11, 8,13,14, 7, 4, 1, 2],
		[0, 4, 8,12, 3, 7,11,15, 6, 2,14,10, 5, 1,13, 9],
		[0, 5,10,15, 7, 2,13, 8,14,11, 4, 1, 9,12, 3, 6],
		[0, 6,12,10,11,13, 7, 1, 5, 3, 9,15,14, 8, 2, 4],
		[0, 7,14, 9,15, 8, 1, 6,13,10, 3, 4, 2, 5,12,11],
		[0, 8, 3,11, 6,14, 5,13,12, 4,15, 7,10, 2, 9, 1],
		[0, 9, 1, 8, 2,11, 3,10, 4,13, 5,12, 6,15, 7,14],
		[0,10, 7,13,14, 4, 9, 3,15, 5, 8, 2, 1,11, 6,12],
		[0,11, 5,14,10, 1,15, 4, 7,12, 2, 9,13, 6, 8, 3],
		[0,12,11, 7, 5, 9,14, 2,10, 6, 1,13,15, 3, 4, 8],
		[0,13, 9, 4, 1,12, 8, 5, 2,15,11, 6, 3,14,10, 7],
		[0,14,15, 1,13, 3, 2,12, 9, 7, 6, 8, 4,10,11, 5],
		[0,15,13, 2, 9, 6, 4,11, 1,14,12, 3, 8, 7, 5,10]]


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

	# print 'k0', key0
	# print 'k1', key1
	# print 'k2', key2

	return (key0, key1, key2)

def mul_s(input):
	r1 = input[0:4]
	r3 = input[4:8]
	r2 = input[8:12]
	r4 = input[12:16]

	s1_temp = int(r1,2)^s_mul[int(r3,2)][4]
	s1 = '{0:0{1}b}'.format(s1_temp,w_len/2)

	s2_temp = int(r2,2)^s_mul[int(r4,2)][4]
	s2 = '{0:0{1}b}'.format(s2_temp,w_len/2)

	s3_temp = s_mul[4][int(r1,2)]^int(r3,2)
	s3 = '{0:0{1}b}'.format(s3_temp,w_len/2)

	s4_temp = s_mul[4][int(r2,2)]^int(r4,2)
	s4 = '{0:0{1}b}'.format(s4_temp,w_len/2)

	return (s1+s3+s2+s4)

def inv_mul_s(input):
	r1 = input[0:4]
	r3 = input[4:8]
	r2 = input[8:12]
	r4 = input[12:16]

	s1_temp = s_mul[9][int(r1,2)]^s_mul[int(r3,2)][2]
	s1 = '{0:0{1}b}'.format(s1_temp,w_len/2)

	s2_temp = s_mul[9][int(r2,2)]^s_mul[int(r4,2)][2]
	s2 = '{0:0{1}b}'.format(s2_temp,w_len/2)

	s3_temp = s_mul[2][int(r1,2)]^s_mul[9][int(r3,2)]
	s3 = '{0:0{1}b}'.format(s3_temp,w_len/2)

	s4_temp = s_mul[2][int(r2,2)]^s_mul[9][int(r4,2)]
	s4 = '{0:0{1}b}'.format(s4_temp,w_len/2)

	return  (s1+s3+s2+s4)


def roundOne(input,key1):
	n1 = input[0:4]
	n2 = input[4:8]
	n3 = input[8:12]
	n4 = input[12:16]

	r1 = s_box[n1]
	r2 = s_box[n2]
	r3 = s_box[n3]
	r4 = s_box[n4]

	re = r1+r4+r3+r2
	# print "s box ", re
	mul_out = mul_s(re)

	# print "mul_out",mul_out


	re_temp = int(mul_out,2)^int(key1,2);
	return '{0:0{1}b}'.format(re_temp,w_len*2)

def roundTwo(input, key2):
	r1 = s_box[input[0:4]]
	r2 = s_box[input[4:8]]
	r3 = s_box[input[8:12]]
	r4 = s_box[input[12:16]]

	temp_out = r1+r4+r3+r2;
	re_temp = int(temp_out,2)^int(key2,2);

	re = '{0:0{1}b}'.format(re_temp,w_len*2)
	
	return re


	

def encrypt(plain_text, key1, key2):
	output1 = roundOne(plain_text,key1)
	output2 = roundTwo(output1, key2)
	return output2


def decrypt(c_text, key0, key1, key2):

	r2_inv = int(c_text,2)^int(key2,2)
	r2 =  '{0:0{1}b}'.format(r2_inv,w_len*2)
	# print "dr2", r2

	shift_inv = r2[0:4]+r2[12:16]+r2[8:12]+r2[4:8]
	# print "shift_inv", shift_inv

	sbox_inv = s_inv[shift_inv[0:4]]+s_inv[shift_inv[4:8]]+s_inv[shift_inv[8:12]]+s_inv[shift_inv[12:16]]

	# print "sbox_inv"

	r1_inv = int(sbox_inv,2)^int(key1,2)
	r1 =  '{0:0{1}b}'.format(r1_inv,w_len*2)
	# print "r1", r1

	inv_mix = inv_mul_s(r1)

	shift_inv1 = inv_mix[0:4]+inv_mix[12:16]+inv_mix[8:12]+inv_mix[4:8]
	# print "shift_inv1", shift_inv1

	sbox_inv1 = s_inv[shift_inv1[0:4]]+s_inv[shift_inv1[4:8]]+s_inv[shift_inv1[8:12]]+s_inv[shift_inv1[12:16]]
	# print "sbox_inv1",sbox_inv1


	r0_inv = int(sbox_inv1,2)^int(key0,2)
	r0 =  '{0:0{1}b}'.format(r0_inv,w_len*2)
	# print "plain_text_recoverd", r0

	return r0
	



w_len = 8
if __name__=='__main__':

	# master_key = '0100101011110101'
	# plain_text = '1111111111111111'

	master_key = raw_input("Enter key:	")
	plain_text = raw_input("Enter Plain Text:	")

	keys = generate_keys(master_key)

	key0 = keys[0]
	key1 = keys[1]
	key2 = keys[2]


	re_temp = int(plain_text,2)^int(key0,2)
	input1 = '{0:0{1}b}'.format(re_temp,w_len*2)
	# print "xor1 ", input1

	cipher_text = encrypt(input1, key1, key2)
	recovered_text = decrypt(cipher_text, key0, key1, key2)

	print "\n"
	print "key Entered:	", master_key
	print "original plain text:	", plain_text
	print "cipher text:	", cipher_text
	print "recovered_text:	", recovered_text

	



	