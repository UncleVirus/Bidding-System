window.addEventListener('DOMContentLoaded', () => {
    const artworks = document.querySelectorAll('.artwork');
    
    artworks.forEach(artwork => {
      artwork.addEventListener('mouseover', () => {
        artworks.forEach(otherArtwork => {
          if (otherArtwork !== artwork) {
            otherArtwork.classList.add('smaller');
          }
        });
      });
      
      artwork.addEventListener('mouseout', () => {
        artworks.forEach(otherArtwork => {
          otherArtwork.classList.remove('smaller');
        });
      });
    });
  });