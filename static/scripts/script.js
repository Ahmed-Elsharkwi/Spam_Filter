
document.addEventListener('DOMContentLoaded', async function() {
    await fetch('http://localhost:5000/spam_filter/user_info', {
                            credentials: 'include',
	})
        .then(response => response.json())
        .then(data => {
            console.log(data);
            const imageUrl = data.state.photo_url;
            const imageContainer = document.getElementById('profile_photo');

            const img = document.createElement('img');
            img.src = imageUrl;
            img.alt = 'Loaded Image';
            
            imageContainer.appendChild(img);
	    img.style.display = 'block';

	    const email = document.getElementById('Email');
	    const Name = document.getElementById('Name');
	    const user_name = document.getElementById('user_Name');

	    email.innerText = `Email_address: ${data.state.email_address}`;
	    Name.innerText = `User_name: ${data.state.name}`;
	    user_Name.innerText = `User_name: ${data.state.name}`;
        })
        .catch(error => console.error('Error fetching data:', error));

    fetch('http://localhost:5000/spam_filter/user_emails', {
	     credentials: 'include',
     })
     .then(response => response.json())
     .then(data => {
	   const image = document.getElementById('image');
	   const dataBlockes = document.getElementById('emails-box');

	   if (data.state == "there are not any blocked emails"){
		image.style.display = 'block';
	        dataBlockes.style.display = 'none';
	   }
	   else{
	     	for (const key in data) {
                    if (data.hasOwnProperty(key)) {
                        const emailInfo = data[key];
                        const emailBox = document.createElement('div');
                        emailBox.className = 'email-box';
                        emailBox.id = key;
                        emailBox.innerHTML = `
                            <p>Email: ${emailInfo.email_address}</p>
			    <div class="icons">
            			<button onclick="editEmail('${key}')">
                			<i class="fas fa-pen"></i>
            			</button>
            			<button onclick="deleteEmail('${key}')">
                			<i class="fas fa-trash"></i>
            			</button>
        		    </div>
                        `;
                        dataBlockes.appendChild(emailBox);
		    }
		};
	        image.style.display = 'none';
	   }
     });
     pop_window = document.getElementById('popupWindow');
     pop_window.style.display = 'none';
});

async function handleClick_Add() {
   const blocked_email = document.getElementById('blocked_email').value
   const data = {"email_address": blocked_email}

   await fetch('http://localhost:5000/spam_filter/new_email', {
	   method: 'POST',
	   credentials: 'include',
	   headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)

   })
   .then(response => response.json())
   .then(data => {
	alert(data.state)
   })
   .catch(error => console.error('Error feching data:', error));

   window.location.href = "http://localhost:8000/user_profile";
};



async function editEmail(key) {
    const pop_window = document.getElementById('popupWindow');
    pop_window.style.display = 'block';
    setTimeout(() => {
        pop_window.classList.add('show');
    }, 10); // Small delay to ensure the transition is applied

    const buttonsumbit = document.getElementById('sumbit');
    buttonsumbit.id = key;
}


function handleClick_No(answer) {
        document.getElementById('popupWindow').classList.remove('show');
        email = document.getElementById('update_email').value;
        let url = 'http://localhost:5000/spam_filter/new_email'; // Replace with your actual API endpoint
        let data = {"email_address": email, "old_id": answer.id}; // Replace with your actual data

            fetch(url, {
                method: 'PUT',
		credentials: 'include',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => data)
            .catch((error) => console.error('Error:', error));
	    window.location.href = "http://localhost:8000/user_profile";
}

function deleteEmail(key) {
	let url = 'http://localhost:5000/spam_filter/user_email_not_exist';
	let data = {"email_id": key}; // Replace with your actual data

            fetch(url, {
                method: 'DELETE',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
		    alert(data.state)})
            .catch((error) => console.error('Error:', error));
            window.location.href = "http://localhost:8000/user_profile";
}

