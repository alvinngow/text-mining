import logo from './logo.svg';
import './App.css';
import { useRef, useState } from 'react';
import { getDefaultNormalizer } from '@testing-library/react';
import { Spin } from 'antd';

function App() {
	async function getLDA() {
		console.log(inputRef.current.value);
		const sentence = inputRef.current.value;
		const response = await fetch(
			`http://127.0.0.1:9001/lda_demo?sentence=${sentence}`
		);
		return response.json();
	}
	async function getSA() {
		console.log(inputRef.current.value);
		const sentence = inputRef.current.value;
		const response = await fetch(
			`http://127.0.0.1:9001/sa_demo?sentence=${sentence}`
		);
		return response.json();
	}
	async function getLDAData() {
		setLDA(await getLDA());
	}
	async function getSAData() {
		setSA(await getSA());
	}
	function handleClick() {
		setLoading(true);
		setLDA(undefined);
		setSA(undefined);
		getLDAData();
		getSAData();
	}

	const [LDA, setLDA] = useState(undefined);
	const [SA, setSA] = useState(undefined);
	const [loading, setLoading] = useState(false);
	console.log(LDA);

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

			{SA && (
				<div className='App-header mt-2 flex justify-center'>
					<div>
						Log:
						{SA.log_pred == 1 ? (
							<p className='text-green-400'>Positive</p>
						) : (
							<p className='text-red-400'>Negative</p>
						)}
					</div>
					<div className='ml-4'>
						SVC:
						{SA.svc_pred == 1 ? (
							<p className='text-green-400'>Positive</p>
						) : (
							<p className='text-red-400'>Negative</p>
						)}
					</div>
				</div>
			)}
			{LDA ? (
				<div className='App-header mt-6'>
					<h2 className='text text-5xl'>LDA</h2>

					<div className='grid grid-cols-[1fr_1fr] mt-2 p-4'>
						<div className='pb-2' style={{ borderBottom: '1px solid white' }}>
							<h2 className='text-header-color'>Untuned LDA</h2>
							{Object.keys(LDA.untuned_topics).map((itemKey) => {
								return (
									<div className='flex justify-center'>
										<div className='text-sm text-center'>
											{itemKey}: {LDA.untuned_topics[itemKey]}
										</div>
									</div>
								);
							})}
						</div>
						<div className='pb-2' style={{ borderBottom: '1px solid white' }}>
							<div className='text-header-color'>Predicted Topic</div>
							<div>{LDA.untuned_prob}</div>
							<p className='text-header-color'>Docs in Topic</p>
							<div className='text-sm'>
								{LDA.untuned_example.map((example) => {
									return <p>{example}</p>;
								})}
							</div>
						</div>
						<div className='mt-2'>
							<div className='text-header-color'>Tuned LDA</div>
							{Object.keys(LDA.best_lda_topics).map((itemKey) => {
								return (
									<div className='flex justify-center'>
										<div className='text-sm text-center'>
											{itemKey}: {LDA.best_lda_topics[itemKey]}
										</div>
									</div>
								);
							})}
						</div>
						<div className='mt-2'>
							<div className='text-header-color'>Predicted Topic</div>
							<div>{LDA.best_prob}</div>
							<p className='text-header-color'>Docs in Topic</p>
							<div className='text-sm'>
								{LDA.best_lda_example.map((example) => {
									return <p>{example}</p>;
								})}
							</div>
						</div>
					</div>
				</div>
			) : loading === true ? (
				<Spin
					style={{ width: '1000px', margin: 'auto', color: 'white' }}
					tip='Loading'
				></Spin>
			) : (
				''
			)}
		</div>
	);
}

export default App;
