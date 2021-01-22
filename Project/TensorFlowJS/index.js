let net;

// async function app() {
//   console.log('Loading mobilenet..');
//
//   // Load the model.
//   net = await mobilenet.load();
//   console.log('Successfully loaded model');
//
//   // Make a prediction through the model on our image.
//   const imgEl = document.getElementById('img');
//   const result = await net.classify(imgEl);
//   // alert(result);
//   console.log(result);
//   console.log("done")
// }


const classifier = knnClassifier.create();
const webcamElement = document.getElementById('webcam');
// webcamElement.width = 100;
// webcamElement.height = 100;

async function app() {
  console.log('Loading mobilenet..');

  // Load the model.
  net = await mobilenet.load();
  console.log('Successfully loaded model');

  // Create an object from Tensorflow.js data API which could capture image
  // from the web camera as Tensor.


  const videoElement = document.createElement('video');

  // const cam = await tf.data.webcam(videoElement);
  // const img = await cam.capture();
  // img.print();
  // cam.stop();

  const webcam = await tf.data.webcam(webcamElement);

  // Reads an image from the webcam and associates it with a specific class
  // index.
  const addExample = async classId => {
    // Capture an image from the web camera.
    const img = await webcam.capture();

    // Get the intermediate activation of MobileNet 'conv_preds' and pass that
    // to the KNN classifier.
    const activation = net.infer(img, true);

    // Pass the intermediate activation to the classifier.
    classifier.addExample(activation, classId);

    // Dispose the tensor to release the memory.
    img.dispose();
  };

  // When clicking a button, add an example for that class.
  document.getElementById('class-a').addEventListener('click', () => addExample(0));
  document.getElementById('class-b').addEventListener('click', () => addExample(1));
  document.getElementById('class-c').addEventListener('click', () => addExample(2));

  while (true) {
    if (classifier.getNumClasses() > 0) {
      const img = await webcam.capture();

      // Get the activation from mobilenet from the webcam.
      const activation = net.infer(img, 'conv_preds');
      // Get the most likely class and confidence from the classifier module.
      const result = await classifier.predictClass(activation);

      const classes = ['A', 'B', 'C'];
      document.getElementById('console').innerText = `
        prediction: ${classes[result.label]}\n
        probability: ${result.confidences[result.label]}
      `;

      // Dispose the tensor to release the memory.
      img.dispose();
    }

    await tf.nextFrame();
  }
}

app();
