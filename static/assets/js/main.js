$(document).ready(function () {
  var a = {};

  a.clock = {
    init: function () {
      this.tick();
    },

    tick: function () {
      with (new Date()) {
        var h, m, s;

        h = 30 * ((getHours() % 12) + getMinutes() / 60);
        m = 6 * getMinutes();
        s = 6 * getSeconds();

        $(".h_pointer").attr("transform", "rotate(" + h + ", 50, 50)");
        $(".m_pointer").attr("transform", "rotate(" + m + ", 50, 50)");
        $(".s_pointer").attr("transform", "rotate(" + s + ", 50, 50)");

        setTimeout(a.clock.tick, 1000);
      }
    },
  };

  // a.setup.init();
  a.clock.init();
});

// Select text from input
const search_button = document.getElementById("search-button");

// When search button is clicked, GET request is sent to server
function searchMarginalia(event) {
  if (event.key == "Enter") {
    let search_query = document.getElementById("search-bar").value;
    console.log(search_query);
    // replace spaces with +
    search_query = search_query.replace(/\s/g, "+");
    const url = `https://moonjump.app/search?query=${search_query}`;
    alert(url);
    console.log(url);
    window.location.href = url;
  }
}

function key_down(e) {
  if (e.key === "Enter") {
    alert(e.key);
    search_func();
  }
}

function search_func() {
  alert(url);
  var query = document.getElementById("search-bar").value;
  query = query.replace(/\s/g, "+");
  const url = `https://moonjump.app/search?query=${query}`;
  // window.location.href = url;
}

function search(ele) {
  if (e.key == "Enter") {
    let query = ele.value;
    query = query.replace(/\s/g, "+");
    const url = `https://moonjump.app/search?query=${query}`;
    console.log(url);
    alert(url);
    window.location.href = url;
  }
}

search_button.addEventListener("click", function () {
  let search_query = document.getElementById("search-bar").value;
  // replace spaces with +
  search_query = search_query.replace(/\s/g, "+");
  let url = `https://moonjump.app/search?query=${search_query}`;
  window.location.href = url;
});

const form = document.getElementById("form");
const search_field = document.getElementById("search-bar").value;

// When search button is clicked, GET request is sent to server
// function searchMarginalia(event) {
//   if (event.key == "Enter") {
//     let search_query = document.getElementById("search-bar").value;
//     console.log(search_query);
//     // replace spaces with +
//     search_query = search_query.replace(/\s/g, "+");
//     const url = `https://moonjump.app/search?query=${search_query}`;
//     console.log(url);
//     window.location.href = url;
//   }

function submitForm(event) {
  event.preventDefault();
  let search_query = document.getElementById("search-bar").value;
  // replace spaces with +
  search_query = search_query.replace(/\s/g, "+");
  const url = `https://moonjump.app/search?query=${search_query}`;
  console.log(url);
  // alert(url);
  window.location.href = url;
}

form.addEventListener("submit", submitForm);
