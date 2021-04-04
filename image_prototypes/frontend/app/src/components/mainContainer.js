import TotalsDisplay from './totalsDisplay'
import DisplayContainer from './infoDisplay/displayContainer'
import '../css/main.css'

function MainContainer(props) {
    return(
        <div className="main">
            <TotalsDisplay/>
            <DisplayContainer/>
        </div>
    )
}

export default MainContainer