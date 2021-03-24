import './App.css';
import TopBar from './components/topBar'
import MainContainer from './components/mainContainer'
import { useState } from 'react';

function App() {

  const [globalUser, setGlobalUser] = useState(null)

  function setUser(userid) {
    setGlobalUser(userid)
  }

  return (
    <div className="App">
      {/* select user from somewhere here - maybe jsut a text field */}
      <TopBar setUser={setUser}/>
      <MainContainer user={globalUser}/>
    </div>
  );
}

export default App;

