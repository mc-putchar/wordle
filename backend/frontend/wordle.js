const WORD_LEN = 5;
const TOAST_DELAY = 5000;
const user_token = "blabla"
let currentRow = 0;
let currentCell = 0;

String.prototype.replaceAt = function(index, replacement) {
	return this.substring(0, index) + replacement + this.substring(index + replacement.length);
}

function toast(message) {
	const bar = document.getElementById("snackbar");
	bar.textContent = message;
	bar.className = "show";
	setTimeout(function() { bar.className = ""; }, TOAST_DELAY);
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
	if (currentCell < WORD_LEN) {
		const board = document.getElementById("gameboard");
		board.rows[currentRow].cells[currentCell].textContent = "[" + this.textContent + "]";
		++currentCell;
	}
}

function onDelete() {
	const board = document.getElementById("gameboard");
	if (currentCell > 0) {
		--currentCell;
	}
	board.rows[currentRow].cells[currentCell].textContent = "[ ]";
}

async function onReturn() {
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
			body: JSON.stringify({token: user_token, attempt: word})
		});
		const data = await response.json();
		const result = data.result;
		for (let i = 0; i < 5; ++i) {
			this.setKeyState(word[i], result[i]);
		}
		this.updateKeys();
		currentCell = 0;
		++currentRow;
		if (data.status === "correct") {
			toast("You won!");
		} else if (data.status == "loser") {
			toast("You lose!");
		}
		updateWordDisplay(result);
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
	}
	setKeyState(key, state) {
		for (let i = 0; i < this.keyrows.length; ++i) {
			for (let j = 0; j < this.keyrows[i].length; ++j) {
				if (this.keyrows[i][j] === key) {
					this.keystates[i] = this.keystates[i].replaceAt(j, getKeyState(state));
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
};

document.addEventListener("DOMContentLoaded", function() {
	const keyboard = new Keyboard();
	const page = document.getElementById("keyboard");
	page.appendChild(keyboard.element);
});
