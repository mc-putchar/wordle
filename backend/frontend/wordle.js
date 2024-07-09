const WORD_LEN = 5;
const MAX_ATTEMPTS = 6;
const TOAST_DELAY = 4000;

let gameState = 0;
let currentRow = 0;
let currentCell = 0;

String.prototype.replaceAt = function(index, replacement) {
	return this.substring(0, index) + replacement + this.substring(index + replacement.length);
}

function toast(message, style = "show", delay = TOAST_DELAY) {
	const bar = document.getElementById("snackbar");
	bar.textContent = message;
	bar.className = style;
	return (setTimeout(function() { bar.className = ""; }, delay));
}

function generateUUID() {
	const cryptoObj = window.crypto || window.msCrypto; // for IE 11
	const array = new Uint8Array(16);
	cryptoObj.getRandomValues(array);

	// Transform to UUID format
	array[6] = (array[6] & 0x0f) | 0x40;
	array[8] = (array[8] & 0x3f) | 0x80;

	const uuid = [...array].map((b, i) => (i === 4 || i === 6 || i === 8 || i === 10 ? '-' : '') + b.toString(16).padStart(2, '0')).join('');
	return uuid;
}

function getToken() {
	let uniqueToken = localStorage.getItem("uniqueToken");
	if (!uniqueToken) {
		uniqueToken = generateUUID();
		localStorage.setItem("uniqueToken", uniqueToken);
	}
	return uniqueToken;
}

function getKeyState(state) {
	if (state === "absent")
		return '0';
	if (state === "present")
		return '2';
	if (state === "correct")
		return '3';
	return '1';
}

function allowReset() {
	const element = document.getElementById("reboot");
	element.className = "show";
}

function updateWordDisplay(result) {
	if (!result) {
		console.log("No result");
		return;
	}
	console.log(result);
	const board = document.getElementById("gameboard");
	const row = board.rows[currentRow - 1];
	for (let i = 0; i < Object.keys(result).length; ++i) {
		if (result[Object.keys(result)[i]] == "absent")
			row.cells[i].className = "letter-absent";
		else if (result[Object.keys(result)[i]] == "present")
			row.cells[i].className = "letter-present";
		else if (result[Object.keys(result)[i]] == "correct")
			row.cells[i].className = "letter-correct";
	}
}

function updateWordDisplay(result) {
	console.log(result);
	if (!result) {
		console.log("No result");
		return;
	}
	const board = document.getElementById("gameboard");
	const row = board.rows[currentRow - 1];
	for (let i = 0; i < Object.keys(result).length; ++i) {
		if (result[Object.keys(result)[i]] == "absent")
			row.cells[i].className = "letter-absent";
		else if (result[Object.keys(result)[i]] == "present")
			row.cells[i].className = "letter-present";
		else if (result[Object.keys(result)[i]] == "correct")
			row.cells[i].className = "letter-correct";
	}
}

function updateWordDisplay(result) {
	console.log(result);
	if (!result) {
		console.log("No result");
		return;
	}
	const board = document.getElementById("gameboard");
	const row = board.rows[currentRow - 1];
	for (let i = 0; i < Object.keys(result).length; ++i) {
		if (result[Object.keys(result)[i]] == "absent")
			row.cells[i].className = "letter-absent";
		else if (result[Object.keys(result)[i]] == "present")
			row.cells[i].className = "letter-present";
		else if (result[Object.keys(result)[i]] == "correct")
			row.cells[i].className = "letter-correct";
	}
}

function updateWordDisplay(result) {
	console.log(result);
	if (!result) {
		console.log("No result");
		return;
	}
	const board = document.getElementById("gameboard");
	const row = board.rows[currentRow - 1];
	for (let i = 0; i < Object.keys(result).length; ++i) {
		if (result[Object.keys(result)[i]] == "absent")
			row.cells[i].className = "letter-absent";
		else if (result[Object.keys(result)[i]] == "present")
			row.cells[i].className = "letter-present";
		else if (result[Object.keys(result)[i]] == "correct")
			row.cells[i].className = "letter-correct";
	}
}

function onKeyClick() {
	if (gameState || currentRow >= MAX_ATTEMPTS)
		return;
	if (currentCell < WORD_LEN) {
		const board = document.getElementById("gameboard");
		board.rows[currentRow].cells[currentCell].textContent = "[" + this.textContent + "]";
		++currentCell;
	}
}

function onDelete() {
	if (gameState || currentRow >= MAX_ATTEMPTS)
		return;
	const board = document.getElementById("gameboard");
	if (currentCell > 0) {
		--currentCell;
	}
	board.rows[currentRow].cells[currentCell].textContent = "[ ]";
}

async function onReturn() {
	if (gameState || currentRow >= MAX_ATTEMPTS)
		return;
	let word = "";
	if (currentCell < WORD_LEN) {
		toast("Not enough letters.");
	} else {
		const board = document.getElementById("gameboard");
		for (let i = 0; i < WORD_LEN; ++i) {
			word += board.rows[currentRow].cells[i].textContent[1];
		}
		const response = await fetch("/word/", {
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json'
			},
			method: "POST",
			body: JSON.stringify({token: getToken(), attempt: word})
		});
		if (response.ok) {
			const data = await response.json();
			if (data.status == "missing") {
				toast("Not in word list");
				return;
			}
			const result = data.result;
			// console.log("attempt: " + data.current_attempt);
			// console.log("currRow: " + currentRow);
			// if (currentRow =! data.current_attempt - 1) {
			// 	//readjust cells
			// 	const prev = data.prev;
			// 	if (prev) {
			// 		currentRow = 0;
			// 		for (let attempt of prev) {

			// 		}
			// 	}
			// }
			for (let i = 0; i < 5; ++i) {
				this.setKeyState(word[i], getKeyState(result[i]));
			}
			this.updateKeys();
			currentCell = 0;
			++currentRow;
			if (data.status === "correct") {
				clearTimeout(toast("You won!", style = "won"));
				gameState = 1;
				allowReset();
			} else if (data.status == "loser") {
				clearTimeout(toast("You lose!", style = "lost"));
				gameState = -1;
				allowReset();
			}
			updateWordDisplay(result);
		} else {
			console.error("POST request failed");
		}
	}
}

class Keyboard {
	constructor() {
		this.element = document.createElement("table");
		this.element.id = "key_table";
		this.keyrows = ["qwertyuiop1", "asdfghjkl 0", "zxcvbnm    "];
		this.keystates = ["1111111111s", "111111111ss", "1111111ssss"];
		this.keyrows.forEach(row => {
			const trow = document.createElement("tr");
			for (let i = 0; i < row.length; i++) {
				const col = document.createElement("td");
				const btn = document.createElement("button");
				btn.className = "key";
				switch (row[i]) {
					case '0':
						btn.textContent = "⏎";
						btn.id = "enter";
						btn.addEventListener('click', onReturn.bind(this));
						break;
					case '1':
						btn.textContent = "←";
						btn.id = "backspace";
						btn.addEventListener('click', onDelete.bind(btn));
						break;
					case ' ':
						btn.className = "spacer";
						break;
					default:
						btn.textContent = row[i];
						btn.id = row[i];
						btn.addEventListener('click', onKeyClick.bind(btn));
						break;
				}
				col.appendChild(btn);
				trow.appendChild(col);
			}
			this.element.appendChild(trow);
		});
		document.addEventListener("keyup", event => this.onKeyUp(event));
		const resetbtn = document.getElementById("resetbtn");
		resetbtn.onclick = this.reset.bind(this);
	}
	setKeyState(key, state) {
		for (let i = 0; i < this.keyrows.length; ++i) {
			for (let j = 0; j < this.keyrows[i].length; ++j) {
				if (this.keyrows[i][j] === key) {
					if (this.keystates[i][j] == "1" || this.keystates[i][j] < state)
						this.keystates[i] = this.keystates[i].replaceAt(j, state);
					return;
				}
			}
		}
	}
	updateKeys() {
		const table = document.getElementById("keyboard").querySelector("table");
		for (let i = 0; i < 3; ++i) {
			for (let j = 0; j < this.keyrows[i].length; ++j) {
				const btn = table.rows[i].cells[j].querySelector("button");
				if (!btn)	continue;
				switch (this.keystates[i][j]) {
					case '0':
						btn.className = "key-absent";
						break;
					case '1':
						btn.className = "key";
						break;
					case '2':
						btn.className = "key-present";
						break;
					case '3':
						btn.className = "key-correct";
						break;
					default:
						break;
				}
			}
		}
	}
	onKeyUp(event) {
		const key = event.key;
		if (key.length === 1 && /[a-zA-Z]/.test(key))
			document.getElementById(key.toLowerCase()).click();
		else if (key === 'Backspace')
			document.getElementById("backspace").click();
		else if (key === 'Enter')
			document.getElementById("enter").click();
	}
	reset() {
		this.keystates = ["1111111111s", "111111111ss", "1111111ssss"];
		this.updateKeys();
		const element = document.getElementById("reboot");
		element.className = "";
		currentRow = 0;
		currentCell = 0;
		const board = document.getElementById("gameboard");
		for (let row of board.rows) {
			for(let cell of row.cells) {
				cell.innerText = "[ ]";
				cell.className = "";
			}
		}
		gameState = 0;
		const bar = document.getElementById("snackbar");
		bar.textContent = "";
		bar.className = "";
		localStorage.removeItem("uniqueToken");
	}
};

document.addEventListener("DOMContentLoaded", function() {
	const keyboard = new Keyboard();
	const page = document.getElementById("keyboard");
	page.appendChild(keyboard.element);
});
