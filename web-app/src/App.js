import logo from './logo.svg';
import './App.css';

function App() {
	return (
		<div className='App'>
			<header className='App-header'>
				<div className='block'>
					<label className='block' for='customTweet'>
						Enter custom Tweet
					</label>
					<input className='text-black p-2' type='text' id='customTweet' />
				</div>
			</header>
		</div>
	);
}

export default App;
