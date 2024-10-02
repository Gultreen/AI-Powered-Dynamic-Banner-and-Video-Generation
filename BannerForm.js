import React, { useState } from 'react';

function BannerForm() {
  const [image, setImage] = useState(null);
  const [promoText, setPromoText] = useState("");
  const [theme, setTheme] = useState("Diwali");
  const [useAI, setUseAI] = useState(false);
  const [generateVideo, setGenerateVideo] = useState(false);
  const [bannerUrl, setBannerUrl] = useState(null);
  const [videoUrl, setVideoUrl] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('image', image);
    formData.append('promoText', promoText);
    formData.append('theme', theme);
    formData.append('useAI', useAI);

    const endpoint = generateVideo ? 'generate_video' : 'generate_banner';

    const response = await fetch(`http://localhost:5000/${endpoint}`, {
      method: 'POST',
      body: formData,
    });

    const result = await response.json();
    if (generateVideo && result.video_url) {
      setVideoUrl(`http://localhost:5000/${result.video_url}`);
    } else if (!generateVideo && result.banner_url) {
      setBannerUrl(`http://localhost:5000/${result.banner_url}`);
    } else {
      alert('Generation failed');
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="image/*" onChange={(e) => setImage(e.target.files[0])} required />
        <input
          type="text"
          value={promoText}
          onChange={(e) => setPromoText(e.target.value)}
          placeholder="Enter Promo Text"
          required
        />
        <select value={theme} onChange={(e) => setTheme(e.target.value)} disabled={useAI}>
          <option value="Diwali">Diwali</option>
          <option value="Independence Day">Independence Day</option>
        </select>
        <label>
          <input type="checkbox" checked={useAI} onChange={() => setUseAI(!useAI)} /> Use AI for Generation
        </label>
        <label>
          <input type="checkbox" checked={generateVideo} onChange={() => setGenerateVideo(!generateVideo)} /> Generate Video
        </label>
        <button type="submit">Generate</button>
      </form>

      {bannerUrl && (
        <div>
          <h3>Generated Banner:</h3>
          <img src={bannerUrl} alt="Generated Banner" style={{ width: "80%" }} />
        </div>
      )}

      {videoUrl && (
        <div>
          <h3>Generated Video:</h3>
          <video width="80%" controls>
            <source src={videoUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
      )}
    </div>
  );
}

export default BannerForm;
