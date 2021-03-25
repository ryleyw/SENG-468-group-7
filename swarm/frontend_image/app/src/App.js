import './App.css';
import TopBar from './components/topBar'
import MainContainer from './components/mainContainer'
import { useState } from 'react';

function App() {

  const [globalUser, setGlobalUser] = useState(null)
  const [userInfo, setUserInfo] = useState(null)

  function setUser(userid) {
    setGlobalUser(userid)
  }

  function setInfo(info) {
    setUserInfo(info)
  }

  return (
    <div className="App">
      {/* select user from somewhere here - maybe jsut a text field */}
      <TopBar setUser={setUser} setInfo={setInfo}/>
      <MainContainer info={userInfo} user={globalUser} setInfo={setInfo}/>
    </div>
  );
}

export default App;

