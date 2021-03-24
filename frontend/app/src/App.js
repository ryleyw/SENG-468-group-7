import logo from './logo.svg';
import './App.css';
import TopBar from './components/topBar'
import MainContainer from './components/mainContainer'

function App() {
  return (
    <div className="App">
      {/* select user from somewhere here - maybe jsut a text field */}
      <TopBar/>
      <MainContainer/>
    </div>
  );
}

export default App;
