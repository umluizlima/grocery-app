(function() {
  if('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js')
             .then(function(registration) {
             console.log('Service Worker Registered');
             return registration;
    })
    .catch(function(err) {
      console.error('Unable to register service worker.', err);
    });
    navigator.serviceWorker.ready.then(function(registration) {
      console.log('Service Worker Ready');
    });
  }
})();

document.addEventListener('DOMContentLoaded', function() {
  read_items();
  const form = document.querySelector('#create-form');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    create_item();
  });
});

const app = document.querySelector('main');
const container = document.createElement('table');
app.insertBefore(container, app.childNodes[0]);

function create_item() {
  var xhr = new XMLHttpRequest();
  xhr.open('POST', document.location + 'list');
  xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
  xhr.onload = function () {
    var data = JSON.parse(xhr.responseText);
    container.insertBefore(card(data), container.childNodes[0]);
  };
  xhr.onerror = function (err) {
    console.error(err, 'issue on POST');
  };
  xhr.send(JSON.stringify({
    content: document.querySelector('#create-content').value
  }));
  document.querySelector('#create-content').value = "";
}

function read_items() {
  var xhr = new XMLHttpRequest();
  xhr.open('GET', document.location + 'list');
  xhr.onload = function () {
    var data = JSON.parse(xhr.responseText);
    data.forEach(function(item) {
      container.appendChild(card(item));
    });
  };
  xhr.onerror = function (err) {
    console.error(err, 'issue on GET');
  };
  xhr.send();
}

function update_item(id) {
  var card = document.getElementById(id);
  content = card.querySelector('.content').textContent;
  done = card.querySelector('.done').checked;

  var xhr = new XMLHttpRequest();
  xhr.open('PUT', document.location + 'list/' + id);
  xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
  xhr.onload = function () {
    var item = document.getElementById(id);
    if (done) {
      container.appendChild(item);
    }
    else {
      container.insertBefore(item, container.childNodes[0]);
    }
  };
  xhr.onerror = function (err) {
    console.error(err, 'issue on PUT');
  };
  xhr.send(JSON.stringify({
    content: content,
    done: done
  }));
}

function delete_item(id) {
  var xhr = new XMLHttpRequest();
  xhr.open('DELETE', document.location + 'list/' + id);
  xhr.onload = function () {
    var item = document.getElementById(id);
    container.removeChild(item);
  };
  xhr.onerror = function (err) {
    console.error(err, 'issue on DELETE');
  };
  xhr.send();
}

function card(item) {
  const card = document.createElement('tr');
  card.setAttribute('id', item.id);
  card.setAttribute('overflow', 'hidden');

  const done = document.createElement('input');
  done.setAttribute('type', 'checkbox');
  done.setAttribute('onClick', 'update_item(' + item.id + ')');
  done.setAttribute('id', 'done' + item.id);
  done.setAttribute('class', 'done');
  if (item.done == true) {
    done.checked = true;
  } else {
    done.checked = false;
  }
  card.appendChild(done);

  const label = document.createElement('label');
  label.setAttribute('for', 'done' + item.id);
  // label.setAttribute('class', 'material-icons');
  // label.textContent = 'checkbox';
  card.appendChild(label);


  const content = document.createElement('p');
  content.setAttribute('class', 'content');
  content.setAttribute('contenteditable', 'true');
  content.setAttribute('onblur', 'update_item(' + item.id + ')');
  content.setAttribute('onsubmit', 'update_item(' + item.id + ')');
  content.textContent = item.content;
  card.appendChild(content);

  const del = document.createElement('button');
  del.setAttribute('onClick', 'delete_item(' + item.id + ')');
  del.setAttribute('class', 'material-icons');
  del.textContent = "delete_outline";
  card.appendChild(del);

  return card;
}

// function refresh_list() {
//   var cards = document.getElementsByClassName('card');
//   while(cards[0]) {
//       cards[0].parentNode.removeChild(cards[0]);
//   }
//   read_items();
// }
