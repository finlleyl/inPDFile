import { useRef, useEffect } from "react";
import { useLoading } from "../../context/LoadingContext";
import LoadingBar from "react-top-loading-bar";

const LoadingTopBar: React.FC = () => {
    const { loading } = useLoading();
    const loadingBarRef = useRef<any>(null);

    useEffect(() => {
        if (loading) {
            loadingBarRef.current?.continuousStart(10, 100);
        } else {
            loadingBarRef.current?.complete();
        }
    }, [loading]);

    return <LoadingBar ref={loadingBarRef} color="#f11946" />;
};

export default LoadingTopBar;
