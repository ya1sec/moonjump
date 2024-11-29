document.addEventListener("DOMContentLoaded", function () {
  const orb = document.querySelector(".orb");
  const orbContainer = document.querySelector(".orb-container");
  const toolbarButtons = document.querySelectorAll(".toolbar-button");

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

  // Handle button hover states on mobile
  toolbarButtons.forEach((button) => {
    // Add pressed state handling
    button.addEventListener("mousedown", function () {
      this.style.transform = "translateY(2px)"; // Subtle downward movement
      this.style.boxShadow = "inset 0 0 5px rgba(255, 255, 255, 0.3)"; // Softer inner shadow
    });

    button.addEventListener("mouseup", function () {
      this.style.transform = "translateY(0)";
      this.style.boxShadow = "none";
    });

    button.addEventListener("click", function () {
      // Remove any hover states
      this.blur(); // Remove focus

      // Force removal of hover state by temporarily disabling pointer events
      this.style.pointerEvents = "none";
      setTimeout(() => {
        this.style.pointerEvents = "auto";
        // Reset transform and shadow after the pointer events are restored
        this.style.transform = "translateY(0)";
        this.style.boxShadow = "none";
      }, 100);

      // Remove any hover-specific classes
      this.classList.remove("hover");
    });

    // Handle touch events
    button.addEventListener(
      "touchstart",
      function () {
        this.style.transform = "translateY(2px)"; // Same subtle movement for touch
        this.style.boxShadow = "inset 0 0 5px rgba(255, 255, 255, 0.3)";
      },
      { passive: true }
    );

    button.addEventListener(
      "touchend",
      function (e) {
        e.preventDefault();
        this.style.transform = "translateY(0)";
        this.style.boxShadow = "none";
        this.click();
      },
      { passive: false }
    );

    // Handle mouse leave during press
    button.addEventListener("mouseleave", function () {
      this.style.transform = "translateY(0)";
      this.style.boxShadow = "none";
    });
  });
});
