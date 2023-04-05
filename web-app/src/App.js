import logo from './logo.svg';
import './App.css';
import { useRef } from 'react';

function App() {
	function runDemo() {
		console.log(inputRef.current.value);
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
						onClick={runDemo}
					>
						Analyse!
					</button>
				</div>
			</header>
		</div>
	);
}

export default App;
