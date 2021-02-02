from discriminator import *
from encoder2decoder import *
from readimg import *
from tqdm import tqdm
import keras

# define the combined generator and discriminator model, for updating the generator
def define_gan(g_model, d_model, image_shape):
	# make weights in the discriminator not trainable
	for layer in d_model.layers:
		if not isinstance(layer, BatchNormalization):
			layer.trainable = False
	# define the source image
	in_src = Input(shape=image_shape)
	# connect the source image to the generator input
	gen_out = g_model(in_src)
	# connect the source input and generator output to the discriminator input
	dis_out = d_model([in_src, gen_out])
	# src image as input, generated image and classification output
	model = Model(in_src, [dis_out, gen_out])
	# compile model
	opt = Adam(lr=0.0002, beta_1=0.5)
	model.compile(loss=['binary_crossentropy', 'mae'], optimizer=opt, loss_weights=[1,100])
	return model

# load and prepare training images
def load_real_samples(filename):
	# load compressed arrays
	data = load(filename)
	# unpack arrays
	X1, X2 = data['arr_0'], data['arr_1']
	# scale from [0,255] to [-1,1]
	X1 = (X1 - 127.5) / 127.5
	X2 = (X2 - 127.5) / 127.5
	return [X1, X2]

# select a batch of random samples, returns images and target
def generate_real_samples(dataset, n_samples, patch_shape_1, patch_shape_2,isRandom=True):
	# unpack dataset
	trainA, trainB = dataset
	# choose random instances
	if isRandom:
		ix = randint(0, trainA.shape[0], n_samples)
	else:
		ix = [1924,662,111,222,333,444]
		ix = ix[:n_samples]
	# retrieve selected images
	X1, X2 = trainA[ix], trainB[ix]
	# generate 'real' class labels (1)
	y = ones((n_samples, patch_shape_1, patch_shape_2, 1))
	return [X1, X2], y

# generate a batch of images, returns images and targets
def generate_fake_samples(g_model, samples, patch_shape_1, patch_shape_2):
	# generate fake instance
	X = g_model.predict(samples)
	# create 'fake' class labels (0)
	y = zeros((len(X), patch_shape_1, patch_shape_2, 1))
	return X, y

# Transform train_on_batch return value
# to dict expected by on_batch_end callback
def named_logs(model, logs):
  result = {}
  for l in zip(model.metrics_names, logs):
    result[l[0]] = l[1]
  return result


# train pix2pix models
def train(d_model, g_model, gan_model, dataset, n_epochs=100, n_batch=1,start=0):
	# determine the output square shape of the discriminator
	n_patch_1 = d_model.output_shape[1]
	n_patch_2 = d_model.output_shape[2]
	# unpack dataset
	trainA, trainB = dataset
	# calculate the number of batches per training epoch
	bat_per_epo = int(len(trainA) / n_batch)
	# calculate the number of training iterations
	n_steps = bat_per_epo * n_epochs
	# manually enumerate epochs
	for i in tqdm(range(n_steps)):
		i = i + number
		# select a batch of real samples
		[X_realA, X_realB], y_real = generate_real_samples(dataset, n_batch, n_patch_1, n_patch_2)
		# generate a batch of fake samples
		X_fakeB, y_fake = generate_fake_samples(g_model, X_realA, n_patch_1, n_patch_2)
		# update discriminator for real samples
		d_loss1 = d_model.train_on_batch([X_realA, X_realB], y_real)

		# update discriminator for generated samples
		d_loss2 = d_model.train_on_batch([X_realA, X_fakeB], y_fake)
		# update the generator
		g_loss, _, _ = gan_model.train_on_batch(X_realA, [y_real, X_realB])
		# summarize performance
		print('>%d, d1[%.3f] d2[%.3f] g[%.3f]' % (i+1, d_loss1, d_loss2, g_loss))

		# if i % 100 ==0 and i!=0:
		# 	print("Save Model...!!!")
		# 	d_model.save("d_model")
		# 	g_model.save("g_model")
		# 	gan_model.save("gan_model")
		# 	break

		# summarize model performance
		if (i) % (bat_per_epo * .5) == 0:
			summarize_performance(i, g_model, d_model, gan_model, dataset, )

# generate samples and save as a plot and save the model
def summarize_performance(step, g_model, d_model, gan_model, dataset, n_samples=3, ):
	# select a sample of input images (fixed sample data for view the progress of model improvement)
	[X_realA, X_realB], _ = generate_real_samples(dataset, n_samples, 1,1,False)
	# generate a batch of fake samples
	X_fakeB, _ = generate_fake_samples(g_model, X_realA, 1,1)
	# scale all pixels from [-1,1] to [0,1]
	X_realA = (X_realA + 1) / 2.0
	X_realB = (X_realB + 1) / 2.0
	X_fakeB = (X_fakeB + 1) / 2.0
	# plot real source images
	for i in range(n_samples):
		pyplot.subplot(3, n_samples, 1 + i)
		pyplot.axis('off')
		pyplot.imshow(X_realA[i])
	# plot generated target image
	for i in range(n_samples):
		pyplot.subplot(3, n_samples, 1 + n_samples + i)
		pyplot.axis('off')
		pyplot.imshow(X_fakeB[i])
	# plot real target image
	for i in range(n_samples):
		pyplot.subplot(3, n_samples, 1 + n_samples*2 + i)
		pyplot.axis('off')
		pyplot.imshow(X_realB[i])
	# save plot to file
	filename1 = 'plot_%06d.png' % (step+1)
	pyplot.savefig(filename1)
	pyplot.close()
	# save the generator model
	g_model.save('g_model_%06d.h5' % (step+1))
	d_model.save('d_model_%06d.h5' % (step+1))
	gan_model.save('gan_model_%06d.h5' % (step+1))
	print('g_model_%06d.h5' % (step+1), 'd_model_%06d.h5' % (step+1), 'gan_model_%06d.h5' % (step+1))

from tensorflow import keras




if __name__ == "__main__":

	LOAD_MODEL = True
	number = 1#12001

	image_shape=(256, 512, 3)
	d_model = define_discriminator(image_shape)
	if LOAD_MODEL : d_model.load_weights("d_model_%06d.h5" % (number))
	print(d_model.summary())


	g_model = define_generator(image_shape)
	if LOAD_MODEL : g_model.load_weights("g_model_%06d.h5" % (number))
	print(g_model.summary())

	gan_model = define_gan(g_model, d_model, image_shape)
	if LOAD_MODEL : gan_model.load_weights("gan_model_%06d.h5" % (number))


	# load real sample and do normalize
	dataset = load_real_samples('cat_256_2000.npz')

	# train model
	train(d_model, g_model, gan_model, dataset,n_batch=2,start=number)