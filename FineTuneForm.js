import React, { useState } from 'react';

function FineTuneForm() {
  const [trainImages, setTrainImages] = useState([]);
  const [trainTexts, setTrainTexts] = useState([""]);

  const handleTrainSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    trainImages.forEach((file) => formData.append('images', file));
    trainTexts.forEach((text) => formData.append('texts', text));

    const response = await fetch('http://localhost:5000/train_model', {
      method: 'POST',
      body: formData,
    });

    const result = await response.json();
    alert(result.message);
  };

  return (
    <div>
      <form onSubmit={handleTrainSubmit}>
        <input type="file" accept="image/*" multiple onChange={(e) => setTrainImages([...e.target.files])} required />
        {trainTexts.map((text, idx) => (
          <input
            key={idx}
            type="text"
            value={text}
            onChange={(e) => {
              const newTrainTexts = [...trainTexts];
              newTrainTexts[idx] = e.target.value;
              setTrainTexts(newTrainTexts);
            }}
            placeholder={`Enter text for image ${idx + 1}`}
            required
          />
        ))}
        <button type="submit">Fine-Tune Model</button>
      </form>
    </div>
  );
}

export default FineTuneForm;
