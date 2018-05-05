document.addEventListener('DOMContentLoaded', function() {
  // console.log('document is ready. I can sleep now');
  read_items();
  const form = document.querySelector('#create-form');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    console.log(document.querySelector('#create-content').value);
    create_item();
  });
});

const app = document.querySelector('main');
const container = document.createElement('div');
container.setAttribute('class', 'container');
app.insertBefore(container, app.childNodes[0]);

function create_item() {
  var xhr = new XMLHttpRequest();
  xhr.open('POST', document.location + 'list');
  xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
  xhr.onload = function (item) {
    container.insertBefore(card(item), container.childNodes[0]);
  };
  xhr.onerror = function (err) {
    requestError(err, 'issue on POST');
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
    requestError(err, 'issue on GET');
  };
  xhr.send();
}

function update_item(id) {
  var card = document.getElementById(id);
  content = card.querySelector('.content').textContent;
  // content = card.childNodes[0].innerHTML;
  done = card.querySelector('.done').checked;
  // done = card.childNodes[1].checked;

  var xhr = new XMLHttpRequest();
  xhr.open('PUT', document.location + 'list/' + id);
  xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
  xhr.onload = refresh_list;
  xhr.onerror = function (err) {
    requestError(err, 'issue on PUT');
  };
  xhr.send(JSON.stringify({
    content: content,
    done: done
  }));
}

function delete_item(id) {
  var xhr = new XMLHttpRequest();
  xhr.open('DELETE', document.location + 'list/' + id);
  xhr.onload = refresh_list;
  xhr.onerror = function (err) {
    requestError(err, 'issue on DELETE');
  };
  xhr.send();
}

function refresh_list() {
  var cards = document.getElementsByClassName('card');
  while(cards[0]) {
      cards[0].parentNode.removeChild(cards[0]);
  }
  read_items();
}

function card(item) {
  const card = document.createElement('div');
  card.setAttribute('class', 'card');
  card.setAttribute('id', item.id);
  card.setAttribute('overflow', 'hidden');

  const done = document.createElement('input');
  done.setAttribute('class', 'done');
  done.setAttribute('type', 'checkbox');
  done.setAttribute('onClick', 'update_item(' + item.id + ')');
  if (item.done == true) {
    done.checked = true;
  } else {
    done.checked = false;
  }
  card.appendChild(done);

  const content = document.createElement('p');
  content.setAttribute('class', 'content');
  content.setAttribute('contenteditable', 'true');
  content.textContent = item.content;
  card.appendChild(content);

  const del = document.createElement('button');
  del.setAttribute('onClick', 'delete_item(' + item.id + ')');
  del.textContent = "X";
  card.appendChild(del);

  return card;
}



// AJAX

// $(document).ready(function() {
//   read_items();
// });

// function create_item() {
  // $.ajax({
  //   url: document.location + 'list',
  //   type: "POST",
  //   contentType: "application/json",
  //   dataType: 'json',
  //   data: JSON.stringify({
  //     content: document.getElementsByName('new_item_content')[0].value
  //   }),
  //   success: function(item) {
  //     container.insertBefore(card(item), container.childNodes[0]);
  //   }
  // });
// }

// function read_items() {
// $.ajax({
//   url: document.location + 'list',
//   type: "GET",
//   dataType: 'json',
//   success: function(data) {
//     data.forEach(function(item) {
//       container.appendChild(card(item));
//     });
//   }
// });
// }

// function read_item(id) {
//   $.ajax({
//     url: document.location + 'list/' + id,
//     type: "GET",
//     dataType: 'json',
//     success: function(item) {
//       container.appendChild(card(item));
//     }
//   });
// }

// function update_item(id) {
//   var card = document.getElementById(id);
//   content = card.childNodes[0].innerHTML;
//   done = card.childNodes[1].checked;
//   $.ajax({
//     url: document.location + 'list/' + id,
//     type: "PUT",
//     contentType: "application/json",
//     dataType: 'json',
//     data: JSON.stringify({
//       content: content,
//       done: done
//     }),
//     success: function(data) {
//       refresh_list();
//     }
//   });
// }

// function delete_item(id) {
//   $.ajax({
//     url: document.location + 'list/' + id,
//     type: "DELETE",
//     dataType: 'json',
//     success: function(data) {
//       refresh_list();
//     }
//   });
// }
