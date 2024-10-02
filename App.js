import React from 'react';
import BannerForm from './components/BannerForm';
import FineTuneForm from './components/FineTuneForm';

function App() {
  return (
    <div className="App">
      <h1>Dynamic Banner and Video Generator</h1>
      <BannerForm />
      <h2>Fine-Tune AI Model</h2>
      <FineTuneForm />
    </div>
  );
}

export default App;
