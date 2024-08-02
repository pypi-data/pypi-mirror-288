document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.querySelector(".chat-form");
    const codeForm = document.querySelector(".code-chat-form");
    const loginForm = document.querySelector(".login-form");
    const messageInput = document.getElementById("message");
    const codeMessageInput = document.getElementById("code-message");
    const output = document.querySelector(".output");
    const codeOutput = document.querySelector(".code-output");

    const spinner = document.getElementById("spinner");
    const codeSpinner = document.getElementById("code-spinner");

    const migrateForm = document.getElementById("migrate_form");

    const designId = document.getElementById("design_id");
    const ddl = document.getElementById("ddl");

    const homeButton = document.getElementById("home-button");
    const manageButton = document.getElementById("manage-button");
    const codeButton = document.getElementById("code-button");
    const homeContainer = document.getElementById("home");
    const manageContainer = document.getElementById("manage");
    const codeContainer = document.getElementById("code");

    homeButton.addEventListener("click", () => {
        homeContainer.classList.remove("hidden");
        manageContainer.classList.add("hidden");
        codeContainer.classList.add("hidden");
    });

    manageButton.addEventListener("click", () => {
        homeContainer.classList.add("hidden");
        manageContainer.classList.remove("hidden");
        codeContainer.classList.add("hidden");
    });

    function sendCheckedValues() {
        const checkboxes = document.querySelectorAll('input[name="checkbox-options"]:checked');
        const checkedValues = Array.from(checkboxes).map(checkbox => checkbox.value);

        // Example endpoint URL
        const endpointUrl = '/manage/ctags';
        token = localStorage.getItem('token');

        // Sending data using fetch API
        fetch(endpointUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ "tables" : checkedValues })
        })
            .then(response => response.json())
            .then(data => console.log('Success:', data))
            .catch(error => console.error('Error:', error));
    }

    function createCheckboxes(array) {
        const container = document.getElementById('checkbox-container');
        container.innerHTML = ''; // Clear any existing checkboxes

        array.forEach(value => {
            const checkboxLabel = document.createElement('label');
            checkboxLabel.textContent = value;

            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.value = value;
            checkbox.name = 'checkbox-options';

            checkbox.addEventListener('change', sendCheckedValues); // Add event listener to each checkbox

            checkboxLabel.prepend(checkbox);
            container.appendChild(checkboxLabel);
            container.appendChild(document.createElement('br'));

        });
    }

    let drawerButton = document.getElementById('toggle-drawer-button')

    function toggleDrawer() {
        const drawerContent = document.getElementById('drawer-content');
        if (drawerContent.classList.contains('hidden')) {
            drawerContent.classList.remove('hidden');
            drawerButton.innerHTML =  "Hide Tools"
        } else {
            drawerContent.classList.add('hidden');
            drawerButton.innerHTML =  "Show Tools"
        }
    }

    drawerButton.addEventListener('click', toggleDrawer);

    codeButton.addEventListener("click", async () => {
        homeContainer.classList.add("hidden");
        manageContainer.classList.add("hidden");
        codeContainer.classList.remove("hidden");

        token = localStorage.getItem('token');
        if (token) {
            const getCtagsResponse = await fetch('/manage/ctags', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!getCtagsResponse.ok) {
                throw new Error(`Error: ${getCtagsResponse.statusText}`);
            }

            const ctags = await getCtagsResponse.json();
            console.log(ctags)
            createCheckboxes(ctags.tables);
        }
    });


        const keyspaceInput = document.getElementById("keyspace");
        const tableInput = document.getElementById("table");
        const sendMessageButton = document.getElementById("send-message");

        function toggleSendMessageButton() {
            if (keyspaceInput.value.trim() !== "" && tableInput.value.trim() !== "") {
                sendMessageButton.disabled = false;
            } else {
                sendMessageButton.disabled = true;
            }
        }

        let lineNumbersCheckbox = document.getElementById("line-numbers");
        lineNumbersCheckbox.addEventListener("change", toggleLineNumbers);

        function toggleLineNumbers() {
            if (lineNumbersCheckbox.checked) {
                fileContent.classList.remove("hidden");
                fileContentNoLineNumbers.classList.add("hidden");
            } else {
                fileContent.classList.add("hidden");
                fileContentNoLineNumbers.classList.remove("hidden");
            }

        }

        keyspaceInput.addEventListener("input", toggleSendMessageButton);
        tableInput.addEventListener("input", toggleSendMessageButton);


        loginForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            const token = document.getElementById("token").value.trim();
            homeContainer.classList.add("hidden");

            if (token) {
                localStorage.setItem('token', token);

                // TODO support database picker
                // Get databases
                const getDatabasesResponse = await fetch('/get_databases', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (!getDatabasesResponse.ok) {
                    throw new Error(`Error: ${getDatabasesResponse.statusText}`);
                }

                const databases = await getDatabasesResponse.json();
                const firstDbId = databases[0]

                // Login to the first database
                const dbLoginResponse = await fetch('/db_login', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({db_id: firstDbId})
                });

                console.log(dbLoginResponse)

                responseJson = await dbLoginResponse.json()
                alert(responseJson.msg)
                homeContainer.classList.add("hidden");
                manageContainer.classList.remove("hidden");
            } else {
                alert('Please enter token.');
            }
        })

        let selectedProgramId = null;

        codeForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            const messageText = codeMessageInput.value.trim();
            if (messageText !== "") {
                // Display the user's message in the chat
                const messageElement = document.createElement("div");
                messageElement.className = "message";
                messageElement.textContent = messageText;
                codeOutput.appendChild(messageElement);

                // Scroll to the bottom of the chat
                codeOutput.scrollTop = output.scrollHeight;

                // Clear the input field
                codeMessageInput.value = "";
                codeSpinner.classList.remove("hidden");

                try {
                    // Send the message to the endpoint
                    let path = `/manage/code`
                    if (selectedProgramId) {
                        path = `/manage/code/${selectedProgramId}`
                    }
                    const response = await fetch(path, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${localStorage.getItem('token')}`
                        },
                        body: JSON.stringify({content: messageText})
                    });

                    // Handle the response from the server
                    if (response.ok) {
                        const data = await response.json();

                        // Display bot response
                        const botMessageElement = document.createElement("div");
                        botMessageElement.className = "message bot-message";
                        botMessageElement.textContent = data[data.length - 1].text;
                        //botMessageElement.textContent = data[0].text;
                        codeOutput.appendChild(botMessageElement);
                        codeOutput.scrollTop = codeOutput.scrollHeight;

                        // Populate file dropdown
                        populateFileDropdown(data);
                    } else {
                        console.error('Error:', response.statusText);
                    }
                } catch (error) {
                    console.error('Error:', error);
                } finally {
                    // Hide the spinner
                    codeSpinner.classList.add("hidden");
                }
            }
        })

        const fileSelect = document.getElementById("file-select");
        const fileContent = document.getElementById("file-content");
        const fileContentNoLineNumbers = document.getElementById("file-content-no-line-numbers");

        function populateFileDropdown(data) {
            // Clear the dropdown
            fileSelect.innerHTML = '<option value="">Select a file</option>';

            // Populate the dropdown with filenames
            data.forEach(programObj => {
                const option = document.createElement("option");
                option.value = programObj.output.filename;
                option.textContent = programObj.output.filename;
                fileSelect.appendChild(option);
            });

            // Set up event listener for file selection
            fileSelect.addEventListener("change", (event) => {
                const selectedFile = event.target.value;
                if (selectedFile) {
                    const selectedOutput = data.find(programObj => programObj.output.filename === selectedFile);
                    selectedProgramId = selectedOutput.program_id;
                    displayFileContent(selectedOutput);
                } else {
                    fileContent.textContent = "";
                    fileContentNoLineNumbers.textContent = "";
                    selectedProgramId = null
                }
            });
            fileContent.textContent = "";
            fileContentNoLineNumbers.textContent = "";
            selectedProgramId = null
        }

        function displayFileContent(programObj) {
            // Display the content of the selected file
            fileContent.textContent = programObj.as_string;
            fileContentNoLineNumbers.textContent = programObj.as_string_no_line_numbers;
        }

        chatForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            const messageText = messageInput.value.trim();
            if (messageText !== "") {
                // Display the user's message in the chat
                const messageElement = document.createElement("div");
                messageElement.className = "message";
                messageElement.textContent = messageText;
                output.appendChild(messageElement);

                // Scroll to the bottom of the chat
                output.scrollTop = output.scrollHeight;

                // Clear the input field
                messageInput.value = "";
                spinner.classList.remove("hidden");

                try {
                    const keyspace_name = document.getElementById("keyspace").value.trim();
                    const table_name = document.getElementById("table").value.trim();

                    // Send the message to the endpoint
                    const response = await fetch(`/manage/${keyspace_name}/${table_name}/design`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${localStorage.getItem('token')}`
                        },
                        body: JSON.stringify({content: messageText})
                    });

                    // Handle the response from the server
                    if (response.ok) {
                        const data = await response.json();
                        const botMessageElement = document.createElement("div");
                        botMessageElement.className = "message bot-message";
                        botMessageElement.textContent = data.diagnosis;
                        designId.value = data.design_id;
                        ddl.value = data.ddl;
                        output.appendChild(botMessageElement);
                        output.scrollTop = output.scrollHeight;
                    } else {
                        console.error('Error:', response.statusText);
                    }
                } catch (error) {
                    console.error('Error:', error);
                } finally {
                    // Hide the spinner
                    spinner.classList.add("hidden");
                }
            }
        });

        migrateForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            const designIdText = designId.value.trim();
            if (designIdText !== "") {
                spinner.classList.remove("hidden");

                try {
                    const keyspace_name = document.getElementById("keyspace").value.trim();
                    const table_name = document.getElementById("table").value.trim();

                    // Send the message to the endpoint
                    const response = await fetch(`/manage/${table_name}/${keyspace_name}/migrate`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${localStorage.getItem('token')}`
                        },
                        body: JSON.stringify({design_id: designIdText})
                    });

                    // Handle the response from the server
                    if (response.ok) {
                        const data = await response.json();
                        console.log(data);
                        alert("Schema migrated successfully.")
                    } else {
                        console.error('Error:', response.statusText);
                    }
                } catch (error) {
                    console.error('Error:', error);
                } finally {
                    // Hide the spinner
                    spinner.classList.add("hidden");
                }
            }
        });
    });
