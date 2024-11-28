document.addEventListener("DOMContentLoaded", function () {
  const orb = document.querySelector(".orb");
  const orbContainer = document.querySelector(".orb-container");

  // Mouse move effect
  document.addEventListener("mousemove", (e) => {
    const { clientX, clientY } = e;
    const rect = orbContainer.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;

    const angleX = (clientY - centerY) * 0.01;
    const angleY = (clientX - centerX) * 0.01;

    orbContainer.style.transform = `perspective(1000px) rotateX(${angleX}deg) rotateY(${angleY}deg)`;
  });

  // Reset position when mouse leaves
  document.addEventListener("mouseleave", () => {
    orbContainer.style.transform = "perspective(1000px) rotateX(0) rotateY(0)";
  });
});
