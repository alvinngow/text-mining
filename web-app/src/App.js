import logo from './logo.svg';
import './App.css';
import { useRef } from 'react';

function App() {
	async function runDemo() {
		console.log(inputRef.current.value);
		const sentence = inputRef.current.value;
		const response = await fetch(
			`http://127.0.0.1:9001/lda_demo?sentence=${sentence}`,
			{
				method: 'GET',
				headers: {
					Accept: 'application/json',
					'Content-Type': 'application/json;charset=UTF-8',
					'Access-Control-Allow-Origin': '*',
				},
			}
		);
		return response;
	}

	async function handleClick() {
		const response = await runDemo();
		const res = await response.json();
		console.log(
			'🚀 ~ file: App.js:25 ~ handleClick ~ response:',
			await response.json()
		);
	}

	const inputRef = useRef();
	return (
		<div className='App'>
			<header className='App-header'>
				<div className='block'>
					<div>
						<label className='block' htmlFor='customTweet'>
							Enter custom Tweet
						</label>
						<input
							ref={inputRef}
							className='text-black p-2'
							type='text'
							id='customTweet'
						/>
					</div>
					<button
						className='bg-blue-500 mt-2 p-2 rounded-3xl'
						onClick={handleClick}
					>
						Analyse!
					</button>
				</div>
			</header>
			<div className='App-header mt-12'>
				<h2 className='text text-5xl'>LDA</h2>
				<div class='grid grid-cols-4 mt-2'>
					<div>
						<h2>Untuned LDA</h2>
					</div>
					<div>Predicted Topic</div>
					<div>Tuned LDA</div>
					<div>Predicted Topic</div>
				</div>
			</div>
		</div>
	);
}

export default App;
