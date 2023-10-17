import React, { useState, useEffect, useContext } from "react";
import { Context } from "../store/appContext";

export const Private = () => {
  const { store, actions } = useContext(Context);

  return (
    <div>
      {store.loggedIn ? (
        <h1>Hello User</h1>
      ) : (
        <h1>Please Login</h1>
      )}
      ;
    </div>
  );
};